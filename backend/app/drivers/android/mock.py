from __future__ import annotations

from dataclasses import dataclass, field

from app.drivers.android.base import AndroidDriver


@dataclass
class MockAndroidDriver(AndroidDriver):
    operations: list[dict] = field(default_factory=list)
    screenshot_count: int = 0

    async def tap_by_text(self, text: str) -> bool:
        self.operations.append({"action": "tap_by_text", "text": text})
        return True

    async def tap_by_resource_id(self, resource_id: str) -> bool:
        self.operations.append({"action": "tap_by_resource_id", "resource_id": resource_id})
        return True

    async def type_text(self, text: str) -> None:
        self.operations.append({"action": "type_text", "text": text})

    async def send_current_text(self) -> bool:
        self.operations.append({"action": "send_current_text"})
        return True

    async def take_screenshot(self) -> str:
        self.screenshot_count += 1
        screenshot_path = f"mock://boss-android/screenshot-{self.screenshot_count}.png"
        self.operations.append({"action": "take_screenshot", "path": screenshot_path})
        return screenshot_path

    async def swipe_up(self) -> None:
        self.operations.append({"action": "swipe_up"})

    async def back(self) -> None:
        self.operations.append({"action": "back"})
