# =============================================================================
# FILE SERVICE - Quản lý file upload/download
# =============================================================================
# Service này xử lý tất cả các thao tác liên quan đến file:
# - Upload file AutoCAD
# - Validate file type
# - Lưu trữ file
# - Download file output
# - Cleanup files cũ

import os  # Để làm việc với file system
import uuid  # Để tạo unique ID
import aiofiles  # Để đọc/ghi file async
from datetime import datetime  # Để lấy thời gian
from typing import Optional, List  # Type hints
from pathlib import Path  # Để làm việc với đường dẫn file
from models.schemas import CADFile, ProcessingStatus  # Import models


class FileService:
    """
    Service quản lý file upload/download cho ứng dụng AutoCAD
    
    Chức năng chính:
    - Upload và validate file AutoCAD
    - Lưu trữ file tạm thời
    - Quản lý file output
    - Cleanup files cũ
    """
    
    def __init__(self, upload_dir: str = "uploads", output_dir: str = "outputs"):
        """
        Khởi tạo FileService
        
        Args:
            upload_dir (str): Thư mục lưu file upload
            output_dir (str): Thư mục lưu file output
        """
        # Thiết lập đường dẫn thư mục
        self.upload_dir = Path(upload_dir)  # Thư mục upload
        self.output_dir = Path(output_dir)  # Thư mục output
        
        # Tạo thư mục nếu chưa tồn tại
        self.upload_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
        
        # Tạo các subdirectories
        (self.upload_dir / "temp").mkdir(exist_ok=True)  # File tạm thời
        (self.output_dir / "2d_files").mkdir(exist_ok=True)  # File 2D output
        (self.output_dir / "downloads").mkdir(exist_ok=True)  # File download
    
    async def save_uploaded_file(self, file_content: bytes, filename: str) -> str:
        """
        Lưu file upload và trả về file ID
        
        Args:
            file_content (bytes): Nội dung file
            filename (str): Tên file gốc
            
        Returns:
            str: File ID duy nhất
            
        Raises:
            ValueError: Nếu file type không được hỗ trợ
        """
        # Tạo unique file ID
        file_id = str(uuid.uuid4())
        file_extension = Path(filename).suffix
        
        # Validate file type (kiểm tra có phải file AutoCAD không)
        if not self._validate_file_type(file_content, file_extension):
            raise ValueError(f"Unsupported file type: {file_extension}")
        
        # Tạo đường dẫn file với file_id
        file_path = self.upload_dir / "temp" / f"{file_id}{file_extension}"
        
        # Lưu file vào storage
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(file_content)
        
        return file_id
    
    def _validate_file_type(self, file_content: bytes, extension: str) -> bool:
        """
        Validate file type dựa trên extension
        
        Args:
            file_content (bytes): Nội dung file
            extension (str): Extension của file
            
        Returns:
            bool: True nếu file type được hỗ trợ
        """
        try:
            # Danh sách các extension được hỗ trợ
            allowed_extensions = ['.dwg', '.dxf', '.dwf', '.stl', '.obj', '.ply']
            return extension.lower() in allowed_extensions
        except Exception:
            return False
    
    def get_file_path(self, file_id: str) -> Optional[Path]:
        """Lấy đường dẫn file từ file ID"""
        temp_dir = self.upload_dir / "temp"
        for file_path in temp_dir.glob(f"{file_id}.*"):
            return file_path
        return None
    
    async def get_file_info(self, file_id: str) -> Optional[CADFile]:
        """Lấy thông tin file"""
        file_path = self.get_file_path(file_id)
        if not file_path or not file_path.exists():
            return None
        
        stat = file_path.stat()
        return CADFile(
            file_id=file_id,
            filename=file_path.name,
            file_size=stat.st_size,
            upload_time=datetime.fromtimestamp(stat.st_ctime).isoformat(),
            status=ProcessingStatus.PENDING,
            file_path=str(file_path)
        )
    
    async def save_output_files(self, job_id: str, files: List[bytes], filenames: List[str]) -> List[str]:
        """Lưu các file output và trả về download URLs"""
        output_dir = self.output_dir / "2d_files" / job_id
        output_dir.mkdir(exist_ok=True)
        
        download_urls = []
        
        for file_content, filename in zip(files, filenames):
            file_path = output_dir / filename
            async with aiofiles.open(file_path, 'wb') as f:
                await f.write(file_content)
            
            # Tạo download URL (trong thực tế sẽ là URL thật)
            download_url = f"/download/{job_id}/{filename}"
            download_urls.append(download_url)
        
        return download_urls
    
    def get_output_files(self, job_id: str) -> List[Path]:
        """Lấy danh sách file output"""
        output_dir = self.output_dir / "2d_files" / job_id
        if not output_dir.exists():
            return []
        
        return list(output_dir.glob("*"))
    
    async def cleanup_temp_files(self, file_id: str):
        """Xóa file tạm thời"""
        file_path = self.get_file_path(file_id)
        if file_path and file_path.exists():
            file_path.unlink()
    
    async def cleanup_old_files(self, max_age_hours: int = 24):
        """Xóa các file cũ"""
        import time
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600
        
        # Cleanup temp files
        temp_dir = self.upload_dir / "temp"
        for file_path in temp_dir.glob("*"):
            if current_time - file_path.stat().st_mtime > max_age_seconds:
                file_path.unlink()
        
        # Cleanup output files
        output_dir = self.output_dir / "2d_files"
        for job_dir in output_dir.iterdir():
            if job_dir.is_dir():
                if current_time - job_dir.stat().st_mtime > max_age_seconds:
                    import shutil
                    shutil.rmtree(job_dir)
