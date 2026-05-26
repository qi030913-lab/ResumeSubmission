from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess
from datetime import UTC, datetime


class ADBError(RuntimeError):
    pass


@dataclass
class ADBClient:
    adb_path: str = "adb"
    device_serial: str | None = None

    def list_devices(self) -> list[str]:
        result = self._run(["devices"])
        lines = result.stdout.splitlines()[1:]
        devices: list[str] = []
        for line in lines:
            if "\tdevice" in line:
                devices.append(line.split("\t", 1)[0].strip())
        return devices

    def shell(self, *args: str) -> str:
        result = self._run(["shell", *args])
        return result.stdout.strip()

    def input_text(self, text: str) -> None:
        self._run(["shell", "input", "text", self.escape_input_text(text)])

    def keyevent(self, key_code: int) -> None:
        self._run(["shell", "input", "keyevent", str(key_code)])

    def swipe(self, start_x: int, start_y: int, end_x: int, end_y: int, duration_ms: int = 300) -> None:
        self._run(
            [
                "shell",
                "input",
                "swipe",
                str(start_x),
                str(start_y),
                str(end_x),
                str(end_y),
                str(duration_ms),
            ]
        )

    def screencap(self, destination_dir: Path) -> str:
        destination_dir.mkdir(parents=True, exist_ok=True)
        file_path = destination_dir / f"adb-screenshot-{datetime.now(UTC).strftime('%Y%m%d%H%M%S%f')}.png"
        args = self._base_args() + ["exec-out", "screencap", "-p"]
        result = subprocess.run(args, capture_output=True, check=False)
        if result.returncode != 0:
            raise ADBError(result.stderr.decode("utf-8", errors="ignore"))
        file_path.write_bytes(result.stdout)
        return str(file_path)

    def current_focus(self) -> str:
        return self.shell("dumpsys", "window", "windows")

    @staticmethod
    def escape_input_text(text: str) -> str:
        replacements = {
            " ": "%s",
            "&": r"\&",
            "<": r"\<",
            ">": r"\>",
            "(": r"\(",
            ")": r"\)",
            ";": r"\;",
            "|": r"\|",
            "*": r"\*",
            "~": r"\~",
            '"': r"\"",
            "'": r"\'",
        }
        escaped = []
        for char in text:
            escaped.append(replacements.get(char, char))
        return "".join(escaped)

    def _run(self, args: list[str]) -> subprocess.CompletedProcess[str]:
        full_args = self._base_args() + args
        result = subprocess.run(full_args, capture_output=True, text=True, check=False)
        if result.returncode != 0:
            raise ADBError(result.stderr.strip() or result.stdout.strip() or "ADB command failed")
        return result

    def _base_args(self) -> list[str]:
        args = [self.adb_path]
        if self.device_serial:
            args.extend(["-s", self.device_serial])
        return args
