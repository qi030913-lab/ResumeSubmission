from app.schemas.platforms import PlatformCreate, PlatformRead


class PlatformService:
    def __init__(self) -> None:
        self._platforms: dict[str, PlatformRead] = {
            "boss_android": PlatformRead(
                platform_code="boss_android",
                platform_name="Boss 直聘 Android",
                platform_family="boss",
                platform_type="android_app",
                adapter_code="boss_android_adapter",
                health_status="healthy",
                supported_actions=["open_job", "start_chat", "send_greeting"],
            )
        }

    def list_platforms(self) -> list[PlatformRead]:
        return list(self._platforms.values())

    def get_platform(self, platform_code: str) -> PlatformRead | None:
        return self._platforms.get(platform_code)

    def create_platform(self, payload: PlatformCreate) -> PlatformRead:
        platform = PlatformRead(**payload.model_dump(), health_status="healthy", supported_actions=[])
        self._platforms[platform.platform_code] = platform
        return platform


platform_service = PlatformService()

