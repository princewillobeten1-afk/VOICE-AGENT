from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from uuid import uuid4


@dataclass(frozen=True)
class StorageObject:
    provider: str
    bucket: str
    object_key: str
    url: str | None = None


@dataclass(frozen=True)
class UploadRequest:
    object_key: str
    content_type: str | None
    size_bytes: int | None
    expires_in_seconds: int = 900


class StorageProviderAdapter:
    name = "base"

    async def create_upload_url(self, request: UploadRequest) -> StorageObject:
        raise NotImplementedError

    async def create_download_url(self, object_key: str, expires_in_seconds: int = 900) -> str:
        raise NotImplementedError

    async def delete_object(self, object_key: str) -> None:
        raise NotImplementedError

    async def copy_object(self, source_key: str, destination_key: str) -> StorageObject:
        raise NotImplementedError


class LocalStorageProvider(StorageProviderAdapter):
    name = "local"

    def __init__(self, root: str = ".voicesense-storage", bucket: str = "local") -> None:
        self.root = Path(root)
        self.bucket = bucket
        self.root.mkdir(parents=True, exist_ok=True)

    async def create_upload_url(self, request: UploadRequest) -> StorageObject:
        target = self.root / request.object_key
        target.parent.mkdir(parents=True, exist_ok=True)
        return StorageObject(provider=self.name, bucket=self.bucket, object_key=request.object_key, url=f"local://upload/{request.object_key}")

    async def create_download_url(self, object_key: str, expires_in_seconds: int = 900) -> str:
        expires_at = int((datetime.now(UTC) + timedelta(seconds=expires_in_seconds)).timestamp())
        return f"local://download/{object_key}?expires={expires_at}"

    async def delete_object(self, object_key: str) -> None:
        target = self.root / object_key
        if target.exists() and target.is_file():
            target.unlink()

    async def copy_object(self, source_key: str, destination_key: str) -> StorageObject:
        return StorageObject(provider=self.name, bucket=self.bucket, object_key=destination_key, url=f"local://copy/{destination_key}")


class PlaceholderCloudStorageProvider(StorageProviderAdapter):
    def __init__(self, name: str, bucket: str) -> None:
        self.name = name
        self.bucket = bucket

    async def create_upload_url(self, request: UploadRequest) -> StorageObject:
        return StorageObject(provider=self.name, bucket=self.bucket, object_key=request.object_key, url=f"https://storage.example/{self.name}/{request.object_key}")

    async def create_download_url(self, object_key: str, expires_in_seconds: int = 900) -> str:
        return f"https://storage.example/{self.name}/{object_key}?signed=true"

    async def delete_object(self, object_key: str) -> None:
        return None

    async def copy_object(self, source_key: str, destination_key: str) -> StorageObject:
        return StorageObject(provider=self.name, bucket=self.bucket, object_key=destination_key)


def object_key_for(workspace_id: str, filename: str) -> str:
    safe_name = filename.replace("/", "_").replace("\\", "_")
    return f"workspaces/{workspace_id}/{uuid4()}-{safe_name}"


def get_storage_provider(provider: str = "local") -> StorageProviderAdapter:
    if provider == "local":
        return LocalStorageProvider()
    if provider in {"s3", "r2", "gcs", "azure"}:
        return PlaceholderCloudStorageProvider(provider, "voicesense-assets")
    raise ValueError(f"Unsupported storage provider: {provider}")