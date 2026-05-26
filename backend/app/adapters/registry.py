from pathlib import Path

from app.adapters.android.boss_android_adapter import BossAndroidAdapter
from app.adapters.base import PlatformAdapter
from app.core.config import get_settings
from app.drivers.android.adb import ADBClient
from app.drivers.android.appium_driver import AppiumAndroidDriver
from app.drivers.android.base import AndroidDriver
from app.drivers.android.mock import MockAndroidDriver
from app.models.entities import Device
from appium.options.android import UiAutomator2Options


class AdapterRegistry:
    def build(self, platform_code: str, platform_type: str, device: Device | None = None) -> tuple[PlatformAdapter, AndroidDriver]:
        if platform_code == "boss_android" and platform_type == "android_app":
            driver = self._build_android_driver(device)
            return BossAndroidAdapter(driver), driver
        raise ValueError(f"Unsupported platform: {platform_code}/{platform_type}")

    def _build_android_driver(self, device: Device | None) -> AndroidDriver:
        settings = get_settings()
        if settings.android_driver_mode == "appium":
            options = UiAutomator2Options()
            options.platform_name = settings.appium_platform_name
            options.automation_name = settings.appium_automation_name
            options.device_name = device.device_name if device else settings.appium_device_name
            options.new_command_timeout = settings.appium_new_command_timeout
            options.no_reset = settings.appium_no_reset
            if settings.appium_app_package:
                options.app_package = settings.appium_app_package
            if settings.appium_app_activity:
                options.app_activity = settings.appium_app_activity
            serial = (device.adb_serial if device else None) or settings.android_default_device_serial
            if serial:
                options.udid = serial

            adb_client = ADBClient(adb_path=settings.android_adb_path, device_serial=serial)
            return AppiumAndroidDriver(
                server_url=settings.appium_server_url,
                options=options,
                adb_client=adb_client,
                artifacts_dir=Path(settings.android_artifacts_dir),
                use_adb_text_input=settings.android_use_adb_text_input,
            )

        return MockAndroidDriver()


adapter_registry = AdapterRegistry()
