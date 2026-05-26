from abc import ABC, abstractmethod


class PlatformAdapter(ABC):
    platform_code: str
    platform_type: str

    @abstractmethod
    async def detect_screen(self) -> str:
        raise NotImplementedError

    @abstractmethod
    async def parse_job(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    async def open_job(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def start_chat(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    async def send_greeting(self, message: str) -> dict:
        raise NotImplementedError

    @abstractmethod
    async def send_resume(self, resume_id: str) -> dict:
        raise NotImplementedError

