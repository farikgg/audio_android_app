from aiofiles import open as async_open
from pathlib import Path
from uuid import uuid4

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
UPLOAD_DIR = PROJECT_ROOT / "media" / "audio"


class LocalStorage:
    def __init__(self) -> None:
        self.upload_dir = UPLOAD_DIR
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    async def save_file(self, filename: str, content: bytes) -> str:
        """Сохраняет байты на диск и возвращает путь к файлу"""

        # получаю расширение (.mp3, .m4a)
        extension = Path(filename).suffix
        if not extension:
            extension = ".m4a"

        # генерирую уникальное имя
        unique_name = f"{uuid4()}{extension}"
        file_path = self.upload_dir / unique_name

        async with async_open(file_path, "wb") as f:
            await f.write(content)

        return str(file_path)
