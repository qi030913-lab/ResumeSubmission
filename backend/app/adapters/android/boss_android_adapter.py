from app.adapters.base import PlatformAdapter
from app.drivers.android.base import AndroidDriver


class BossAndroidAdapter(PlatformAdapter):
    platform_code = "boss_android"
    platform_type = "android_app"

    def __init__(self, driver: AndroidDriver) -> None:
        self.driver = driver

    async def detect_screen(self) -> str:
        return "job_detail"

    async def parse_job(self) -> dict:
        return {
            "platform_code": self.platform_code,
            "title": "unknown",
            "company_name": "unknown",
        }

    async def open_job(self) -> None:
        # Later this method can tap a job card from a list page.
        return None

    async def start_chat(self) -> dict:
        clicked = await self.driver.tap_by_text("立即沟通")
        return {
            "action": "start_chat",
            "status": "success" if clicked else "element_not_found",
            "selector_candidates": [{"text": "立即沟通"}, {"content_desc": "立即沟通"}],
        }

    async def send_greeting(self, message: str) -> dict:
        await self.driver.type_text(message)
        sent = await self.driver.send_current_text()
        return {
            "action": "send_greeting",
            "status": "success" if sent else "send_failed",
            "message_preview": message,
        }

    async def send_resume(self, resume_id: str) -> dict:
        return {
            "action": "send_resume",
            "status": "manual_step_required",
            "resume_id": resume_id,
        }
