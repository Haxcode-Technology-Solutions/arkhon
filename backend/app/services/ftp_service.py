"""FTP service for downloading product feeds."""
import os
import logging
from datetime import datetime
from typing import Optional, Dict, Any
from pathlib import Path
import aiofiles
from aioftp import Client as FTPClient

from app.core.config import settings


logger = logging.getLogger(__name__)


class FTPService:
    """Service for FTP operations."""

    def __init__(self, entity_code: str):
        """Initialize FTP service for specific entity."""
        self.entity_code = entity_code
        self.config = self._get_ftp_config(entity_code)

    def _get_ftp_config(self, entity_code: str) -> Dict[str, Any]:
        """Get FTP configuration for entity."""
        # In production, this would come from database
        if entity_code == "bigbuy":
            return {
                "host": settings.BIGBUY_FTP_HOST,
                "port": settings.BIGBUY_FTP_PORT,
                "user": settings.BIGBUY_FTP_USER,
                "password": settings.BIGBUY_FTP_PASSWORD,
                "path": settings.BIGBUY_FTP_PATH
            }
        else:
            raise ValueError(f"Unknown entity code: {entity_code}")

    async def download_feed(self, remote_filename: str) -> Optional[str]:
        """
        Download feed file from FTP server.

        Returns:
            Local file path if successful, None otherwise
        """
        try:
            # Create local directory structure: feeds/YYYY-MM-DD/{entity}/
            today = datetime.utcnow().strftime("%Y-%m-%d")
            local_dir = Path(settings.LOCAL_STORAGE_PATH) / "feeds" / today / self.entity_code
            local_dir.mkdir(parents=True, exist_ok=True)

            local_filepath = local_dir / remote_filename

            # Skip if already downloaded today
            if local_filepath.exists():
                logger.info(f"File already exists: {local_filepath}")
                return str(local_filepath)

            # Connect to FTP
            async with FTPClient.context(
                self.config["host"],
                port=self.config["port"],
                user=self.config["user"],
                password=self.config["password"]
            ) as client:
                logger.info(f"Connected to FTP: {self.config['host']}")

                # Change to remote directory
                if self.config["path"]:
                    await client.change_directory(self.config["path"])

                # Download file
                remote_path = remote_filename
                logger.info(f"Downloading {remote_path} to {local_filepath}")

                async with aiofiles.open(local_filepath, "wb") as local_file:
                    async for block in client.download_stream(remote_path):
                        await local_file.write(block)

                file_size = local_filepath.stat().st_size
                logger.info(f"Downloaded {remote_filename}: {file_size} bytes")

                return str(local_filepath)

        except Exception as e:
            logger.error(f"FTP download failed: {e}")
            return None

    async def list_files(self, pattern: Optional[str] = None) -> list:
        """List files on FTP server."""
        try:
            async with FTPClient.context(
                self.config["host"],
                port=self.config["port"],
                user=self.config["user"],
                password=self.config["password"]
            ) as client:
                if self.config["path"]:
                    await client.change_directory(self.config["path"])

                files = []
                async for path, info in client.list():
                    if info["type"] == "file":
                        filename = str(path)
                        if pattern is None or pattern in filename:
                            files.append({
                                "name": filename,
                                "size": info.get("size", 0),
                                "modified": info.get("modify", "")
                            })

                return files

        except Exception as e:
            logger.error(f"FTP list failed: {e}")
            return []
