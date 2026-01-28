from aioboto3 import Session
from uuid import uuid4
from pathlib import Path

from src.app.config import get_settings

settings = get_settings().s3_settings


class S3Storage:
    def __init__(self):
        self.access_key: str = settings.access_key
        self.bucket: str = settings.bucket
        self.endpoint_url: str = settings.endpoint_url
        self.secret_key: str = settings.secret_key
        self.session: Session = Session()

    async def save_file(self, filename: str, content: bytes) -> str:
        extension = Path(filename).suffix
        if not extension:
            extension = ".m4a"

        unique_name = f"{uuid4()}{extension}"
        file_path: str = f"audio/{unique_name}"

        async with self.session.client(
            service_name="s3",
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
        ) as s3:
            await s3.put_object(Bucket=self.bucket, Key=file_path, Body=content)

        return file_path

    async def read_file(self, filepath: str) -> bytes:
        async with self.session.client(
            service_name="s3",
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
        ) as s3:
            response = await s3.get_object(Bucket=self.bucket, Key=filepath)
            content = await response["Body"].read()

        return content
