from app.adapters.android.boss_android_adapter import BossAndroidAdapter
from app.adapters.base import PlatformAdapter
from app.drivers.android.mock import MockAndroidDriver


class AdapterRegistry:
    def build(self, platform_code: str, platform_type: str) -> tuple[PlatformAdapter, MockAndroidDriver]:
        if platform_code == "boss_android" and platform_type == "android_app":
            driver = MockAndroidDriver()
            return BossAndroidAdapter(driver), driver
        raise ValueError(f"Unsupported platform: {platform_code}/{platform_type}")


adapter_registry = AdapterRegistry()

