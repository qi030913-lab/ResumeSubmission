from app.adapters.registry import AdapterRegistry
from app.core.config import get_settings
from app.drivers.android.adb import ADBClient
from app.drivers.android.appium_driver import AppiumAndroidDriver
from app.drivers.android.mock import MockAndroidDriver
from app.models.entities import Device


def test_adb_escape_input_text_handles_spaces_and_symbols() -> None:
    escaped = ADBClient.escape_input_text("Hello World&(AI)")
    assert escaped == r"Hello%sWorld\&\(AI\)"


def test_registry_builds_mock_driver_by_default(monkeypatch) -> None:
    monkeypatch.delenv("ANDROID_DRIVER_MODE", raising=False)
    get_settings.cache_clear()

    adapter, driver = AdapterRegistry().build("boss_android", "android_app")

    assert adapter.platform_code == "boss_android"
    assert isinstance(driver, MockAndroidDriver)

    get_settings.cache_clear()


def test_registry_builds_appium_driver_when_enabled(monkeypatch) -> None:
    monkeypatch.setenv("ANDROID_DRIVER_MODE", "appium")
    monkeypatch.setenv("ANDROID_DEFAULT_DEVICE_SERIAL", "serial-from-env")
    monkeypatch.setenv("APPIUM_SERVER_URL", "http://127.0.0.1:4723")
    get_settings.cache_clear()

    device = Device(device_code="pixel7", platform_type="android_app", device_name="Pixel 7", adb_serial="serial-from-device")
    _, driver = AdapterRegistry().build("boss_android", "android_app", device=device)

    assert isinstance(driver, AppiumAndroidDriver)
    assert driver.adb_client.device_serial == "serial-from-device"

    get_settings.cache_clear()
