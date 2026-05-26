from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException, WebDriverException

from app.drivers.android.adb import ADBClient
from app.drivers.android.base import AndroidDriver


class AppiumDriverError(RuntimeError):
    pass


@dataclass
class AppiumAndroidDriver(AndroidDriver):
    server_url: str
    options: UiAutomator2Options
    adb_client: ADBClient
    artifacts_dir: Path
    use_adb_text_input: bool = True
    driver_type: str = "appium_android"
    operations: list[dict[str, Any]] = field(default_factory=list)
    _driver: webdriver.Remote | None = None

    async def tap_by_text(self, text: str) -> bool:
        driver = self._ensure_session()
        try:
            element = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{text}")')
            element.click()
            self.operations.append({"action": "tap_by_text", "text": text, "status": "success"})
            return True
        except NoSuchElementException:
            self.operations.append({"action": "tap_by_text", "text": text, "status": "not_found"})
            return False

    async def tap_by_resource_id(self, resource_id: str) -> bool:
        driver = self._ensure_session()
        try:
            element = driver.find_element(AppiumBy.ID, resource_id)
            element.click()
            self.operations.append({"action": "tap_by_resource_id", "resource_id": resource_id, "status": "success"})
            return True
        except NoSuchElementException:
            self.operations.append({"action": "tap_by_resource_id", "resource_id": resource_id, "status": "not_found"})
            return False

    async def type_text(self, text: str) -> None:
        driver = self._ensure_session()
        self.operations.append({"action": "type_text", "mode": "adb" if self.use_adb_text_input else "appium"})
        if self.use_adb_text_input:
            self.adb_client.input_text(text)
            return

        try:
            active = driver.switch_to.active_element
            active.send_keys(text)
        except WebDriverException as exc:
            raise AppiumDriverError(f"Failed to type text through Appium: {exc}") from exc

    async def send_current_text(self) -> bool:
        sent = await self.tap_by_text("发送")
        if sent:
            self.operations.append({"action": "send_current_text", "mode": "tap_send"})
            return True

        self.adb_client.keyevent(66)
        self.operations.append({"action": "send_current_text", "mode": "adb_enter"})
        return True

    async def take_screenshot(self) -> str:
        driver = self._ensure_session()
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)
        screenshot_path = self.artifacts_dir / "last-appium-screenshot.png"
        try:
            driver.get_screenshot_as_file(str(screenshot_path))
            self.operations.append({"action": "take_screenshot", "path": str(screenshot_path), "mode": "appium"})
            return str(screenshot_path)
        except WebDriverException:
            fallback = self.adb_client.screencap(self.artifacts_dir)
            self.operations.append({"action": "take_screenshot", "path": fallback, "mode": "adb"})
            return fallback

    async def swipe_up(self) -> None:
        driver = self._ensure_session()
        size = driver.get_window_size()
        start_x = int(size["width"] * 0.5)
        start_y = int(size["height"] * 0.75)
        end_y = int(size["height"] * 0.25)
        self.adb_client.swipe(start_x, start_y, start_x, end_y)
        self.operations.append({"action": "swipe_up", "width": size["width"], "height": size["height"]})

    async def back(self) -> None:
        driver = self._ensure_session()
        driver.back()
        self.operations.append({"action": "back"})

    async def close(self) -> None:
        if self._driver is not None:
            self._driver.quit()
            self._driver = None
            self.operations.append({"action": "close"})

    def export_debug_trace(self) -> list[dict]:
        return list(self.operations)

    def _ensure_session(self) -> webdriver.Remote:
        if self._driver is None:
            self._driver = webdriver.Remote(self.server_url, options=self.options)
            self.operations.append({"action": "create_session", "server_url": self.server_url})
        return self._driver
