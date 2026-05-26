from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "resume-automation-api"
    app_env: str = "local"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    database_url: str = "sqlite:///./resume_automation.db"
    database_echo: bool = False
    database_auto_create: bool = True
    database_seed_reference_data: bool = True
    redis_url: str = "redis://localhost:6379/0"
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/1"
    celery_task_always_eager: bool = True
    android_driver_mode: str = "mock"
    android_adb_path: str = "adb"
    android_default_device_serial: str | None = None
    android_artifacts_dir: str = "./artifacts"
    android_use_adb_text_input: bool = True
    appium_server_url: str = "http://127.0.0.1:4723"
    appium_automation_name: str = "UiAutomator2"
    appium_platform_name: str = "Android"
    appium_device_name: str = "Android"
    appium_new_command_timeout: int = 120
    appium_no_reset: bool = True
    appium_app_package: str | None = None
    appium_app_activity: str | None = None


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
