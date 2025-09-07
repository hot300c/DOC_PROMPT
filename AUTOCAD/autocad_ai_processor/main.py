# =============================================================================
# AUTOCAD 3D TO 2D AI PROCESSOR - MAIN APPLICATION
# =============================================================================
# File này là entry point chính của ứng dụng
# Chứa tất cả các API endpoints để xử lý file AutoCAD

# Import các thư viện cần thiết
from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uuid  # Để tạo unique ID cho jobs
import asyncio  # Để xử lý async/await
from datetime import datetime  # Để lấy thời gian hiện tại
from typing import List, Dict, Any  # Để type hints
import logging  # Để ghi log
import os  # Để làm việc với file system

# Import các model (data structures) từ thư mục models
from models.schemas import (
    UploadResponse, ProcessResponse, StatusResponse, DownloadResponse,
    ProcessingStatus, ProcessingJob
)

# Import các service (business logic) từ thư mục services
from services.file_service import FileService  # Quản lý file upload/download
from services.cad_parser import CADParser  # Parse file AutoCAD
from services.component_analyzer import ComponentAnalyzer  # Phân tích components
from services.output_service import OutputService  # Tạo file 2D

# =============================================================================
# CẤU HÌNH LOGGING
# =============================================================================
# Thiết lập logging để ghi lại các hoạt động của ứng dụng
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =============================================================================
# KHỞI TẠO FASTAPI APPLICATION
# =============================================================================
# Tạo ứng dụng FastAPI với metadata
app = FastAPI(
    title="AutoCAD 3D to 2D AI Processor",  # Tên ứng dụng
    description="API for converting AutoCAD 3D files to 2D with AI-powered component naming",  # Mô tả
    version="1.0.0"  # Phiên bản
)

# =============================================================================
# CẤU HÌNH CORS MIDDLEWARE
# =============================================================================
# CORS (Cross-Origin Resource Sharing) cho phép frontend gọi API từ domain khác
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả origins (trong production nên hạn chế)
    allow_credentials=True,  # Cho phép gửi cookies
    allow_methods=["*"],  # Cho phép tất cả HTTP methods
    allow_headers=["*"],  # Cho phép tất cả headers
)

# =============================================================================
# KHỞI TẠO CÁC SERVICES
# =============================================================================
# Tạo instances của các service classes
file_service = FileService()  # Service quản lý file
cad_parser = CADParser()  # Service parse file AutoCAD
component_analyzer = ComponentAnalyzer()  # Service phân tích components
output_service = OutputService()  # Service tạo file 2D

# =============================================================================
# IN-MEMORY STORAGE
# =============================================================================
# Lưu trữ thông tin các job đang xử lý
# Trong production, nên dùng database thay vì memory
processing_jobs: Dict[str, ProcessingJob] = {}


# =============================================================================
# API ENDPOINTS
# =============================================================================

@app.get("/")
async def root():
    """
    Root endpoint - Trang chủ của API
    
    Returns:
        dict: Thông tin cơ bản về API
    """
    return {"message": "AutoCAD 3D to 2D AI Processor API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    """
    Health check endpoint - Kiểm tra tình trạng của API
    
    Returns:
        dict: Trạng thái healthy và timestamp
    """
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.post("/api/cad/upload", response_model=UploadResponse)
async def upload_cad_file(file: UploadFile = File(...)):
    """
    Upload CAD file endpoint - Upload file AutoCAD 3D lên server
    
    Args:
        file (UploadFile): File AutoCAD được upload từ client
        
    Returns:
        UploadResponse: Thông tin về file đã upload (file_id, status, message)
        
    Raises:
        HTTPException: Nếu có lỗi trong quá trình upload
    """
    try:
        # Kiểm tra file có tồn tại không
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Đọc nội dung file
        file_content = await file.read()
        
        # Kiểm tra file có rỗng không
        if len(file_content) == 0:
            raise HTTPException(status_code=400, detail="Empty file")
        
        # Lưu file vào storage và lấy file_id
        file_id = await file_service.save_uploaded_file(file_content, file.filename)
        
        # Ghi log thành công
        logger.info(f"File uploaded successfully: {file_id}")
        
        # Trả về response
        return UploadResponse(
            file_id=file_id,
            status="success",
            message=f"File {file.filename} uploaded successfully"
        )
        
    except Exception as e:
        # Ghi log lỗi và trả về HTTP error
        logger.error(f"Upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/cad/process", response_model=ProcessResponse)
async def process_cad_file(
    file_id: str,
    background_tasks: BackgroundTasks
):
    """
    Start processing CAD file endpoint - Bắt đầu xử lý file AutoCAD
    
    Args:
        file_id (str): ID của file đã upload
        background_tasks (BackgroundTasks): FastAPI background tasks để xử lý async
        
    Returns:
        ProcessResponse: Thông tin về job đã tạo (process_id, status, message)
        
    Raises:
        HTTPException: Nếu file không tồn tại hoặc có lỗi
    """
    try:
        # Kiểm tra file có tồn tại trong storage không
        file_info = await file_service.get_file_info(file_id)
        if not file_info:
            raise HTTPException(status_code=404, detail="File not found")
        
        # Tạo job mới với unique ID
        job_id = str(uuid.uuid4())
        job = ProcessingJob(
            job_id=job_id,
            file_id=file_id,
            status=ProcessingStatus.PENDING,  # Trạng thái chờ xử lý
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        
        # Lưu job vào memory storage
        processing_jobs[job_id] = job
        
        # Bắt đầu xử lý file trong background (không block API response)
        background_tasks.add_task(process_cad_file_background, job_id, file_id)
        
        # Ghi log
        logger.info(f"Processing started for job {job_id}")
        
        # Trả về response ngay lập tức
        return ProcessResponse(
            process_id=job_id,
            status="started",
            message="Processing started successfully"
        )
        
    except Exception as e:
        # Ghi log lỗi và trả về HTTP error
        logger.error(f"Process start error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


async def process_cad_file_background(job_id: str, file_id: str):
    """
    Background task để xử lý file AutoCAD - Chạy trong background không block API
    
    Args:
        job_id (str): ID của job đang xử lý
        file_id (str): ID của file cần xử lý
        
    Workflow:
        1. Parse file AutoCAD bằng external API
        2. Phân tích components với AI
        3. Tạo file 2D
        4. Lưu kết quả
    """
    try:
        # Cập nhật trạng thái job
        job = processing_jobs[job_id]
        job.status = ProcessingStatus.PROCESSING
        job.message = "Parsing CAD file..."
        job.updated_at = datetime.now().isoformat()
        
        # Lấy đường dẫn file từ storage
        file_path = file_service.get_file_path(file_id)
        if not file_path:
            raise Exception("File not found")
        
        # BƯỚC 1: Parse file AutoCAD bằng external API
        job.message = "Extracting components using external API..."
        components = await cad_parser.parse_file(str(file_path), use_external_api=True)
        job.progress = 25  # 25% hoàn thành
        
        # BƯỚC 2: Phân tích components với AI
        job.message = "Analyzing components with AI..."
        processed_components = await component_analyzer.analyze_components(components)
        job.components = processed_components
        job.progress = 75  # 75% hoàn thành
        
        # BƯỚC 3: Tạo file 2D bằng external API
        job.message = "Creating 2D files using external API..."
        output_files = await output_service.create_2d_files(processed_components, job_id, use_external_api=True)
        
        # BƯỚC 4: Lưu file output vào storage
        file_contents = [content for _, content in output_files]  # Lấy nội dung file
        filenames = [filename for filename, _ in output_files]  # Lấy tên file
        download_urls = await file_service.save_output_files(job_id, file_contents, filenames)
        
        # Cập nhật job hoàn thành
        job.output_files = download_urls
        job.status = ProcessingStatus.COMPLETED
        job.progress = 100  # 100% hoàn thành
        job.message = "Processing completed successfully"
        job.updated_at = datetime.now().isoformat()
        
        # Ghi log thành công
        logger.info(f"Processing completed for job {job_id}")
        
    except Exception as e:
        # Xử lý lỗi - cập nhật job status thành FAILED
        logger.error(f"Background processing error for job {job_id}: {e}")
        job = processing_jobs[job_id]
        job.status = ProcessingStatus.FAILED
        job.message = f"Processing failed: {str(e)}"
        job.updated_at = datetime.now().isoformat()


@app.get("/api/cad/process/{process_id}/status", response_model=StatusResponse)
async def get_processing_status(process_id: str):
    """
    Get processing status endpoint - Kiểm tra trạng thái xử lý của job
    
    Args:
        process_id (str): ID của job cần kiểm tra
        
    Returns:
        StatusResponse: Trạng thái hiện tại của job (status, progress, message, components_count)
        
    Raises:
        HTTPException: Nếu job không tồn tại hoặc có lỗi
    """
    try:
        # Tìm job trong memory storage
        job = processing_jobs.get(process_id)
        if not job:
            raise HTTPException(status_code=404, detail="Processing job not found")
        
        # Trả về thông tin trạng thái
        return StatusResponse(
            status=job.status,  # PENDING, PROCESSING, COMPLETED, FAILED
            progress=job.progress,  # 0-100
            message=job.message,  # Thông báo hiện tại
            components_count=len(job.components) if job.components else None  # Số components đã xử lý
        )
        
    except Exception as e:
        # Ghi log lỗi và trả về HTTP error
        logger.error(f"Status check error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/cad/process/{process_id}/download", response_model=DownloadResponse)
async def download_results(process_id: str):
    """
    Download processing results endpoint - Lấy thông tin download của job đã hoàn thành
    
    Args:
        process_id (str): ID của job cần download
        
    Returns:
        DownloadResponse: Danh sách download URLs và thông tin files
        
    Raises:
        HTTPException: Nếu job không tồn tại, chưa hoàn thành hoặc có lỗi
    """
    try:
        # Tìm job trong memory storage
        job = processing_jobs.get(process_id)
        if not job:
            raise HTTPException(status_code=404, detail="Processing job not found")
        
        # Kiểm tra job đã hoàn thành chưa
        if job.status != ProcessingStatus.COMPLETED:
            raise HTTPException(status_code=400, detail="Processing not completed yet")
        
        # Lấy danh sách file output từ storage
        output_files = file_service.get_output_files(process_id)
        
        # Tạo thông tin chi tiết về từng file
        files_info = []
        for file_path in output_files:
            files_info.append({
                "name": file_path.name,  # Tên file
                "type": file_path.suffix[1:] if file_path.suffix else "unknown"  # Loại file (dxf, pdf, etc.)
            })
        
        # Trả về response với download URLs và file info
        return DownloadResponse(
            download_urls=job.output_files,  # URLs để download
            files=files_info  # Thông tin chi tiết files
        )
        
    except Exception as e:
        # Ghi log lỗi và trả về HTTP error
        logger.error(f"Download error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/cad/process/{process_id}/download/{filename}")
async def download_file(process_id: str, filename: str):
    """
    Download specific file endpoint - Download một file cụ thể từ job
    
    Args:
        process_id (str): ID của job
        filename (str): Tên file cần download
        
    Returns:
        FileResponse: File để download
        
    Raises:
        HTTPException: Nếu job không tồn tại, chưa hoàn thành, hoặc file không tồn tại
    """
    try:
        # Tìm job trong memory storage
        job = processing_jobs.get(process_id)
        if not job:
            raise HTTPException(status_code=404, detail="Processing job not found")
        
        # Kiểm tra job đã hoàn thành chưa
        if job.status != ProcessingStatus.COMPLETED:
            raise HTTPException(status_code=400, detail="Processing not completed yet")
        
        # Tìm file cụ thể trong output files
        output_files = file_service.get_output_files(process_id)
        file_path = None
        
        # Duyệt qua tất cả files để tìm file có tên trùng khớp
        for path in output_files:
            if path.name == filename:
                file_path = path
                break
        
        # Kiểm tra file có tồn tại không
        if not file_path or not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        # Trả về file để download
        return FileResponse(
            path=str(file_path),  # Đường dẫn file
            filename=filename,  # Tên file khi download
            media_type='application/octet-stream'  # Loại MIME
        )
        
    except Exception as e:
        # Ghi log lỗi và trả về HTTP error
        logger.error(f"File download error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/cad/process/{process_id}/components")
async def get_components(process_id: str):
    """
    Get processed components endpoint - Lấy danh sách components đã xử lý
    
    Args:
        process_id (str): ID của job
        
    Returns:
        dict: Danh sách components với thông tin chi tiết
        
    Raises:
        HTTPException: Nếu job không tồn tại hoặc có lỗi
    """
    try:
        # Tìm job trong memory storage
        job = processing_jobs.get(process_id)
        if not job:
            raise HTTPException(status_code=404, detail="Processing job not found")
        
        # Kiểm tra có components chưa
        if not job.components:
            return {"components": [], "message": "No components processed yet"}
        
        # Chuyển đổi components thành dictionary để trả về JSON
        return {"components": [comp.dict() for comp in job.components]}
        
    except Exception as e:
        # Ghi log lỗi và trả về HTTP error
        logger.error(f"Get components error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/cad/process/{process_id}")
async def delete_processing_job(process_id: str):
    """
    Delete processing job endpoint - Xóa job và cleanup files
    
    Args:
        process_id (str): ID của job cần xóa
        
    Returns:
        dict: Thông báo xóa thành công
        
    Raises:
        HTTPException: Nếu job không tồn tại hoặc có lỗi
    """
    try:
        # Tìm job trong memory storage
        job = processing_jobs.get(process_id)
        if not job:
            raise HTTPException(status_code=404, detail="Processing job not found")
        
        # Cleanup files tạm thời
        await file_service.cleanup_temp_files(job.file_id)
        
        # Xóa job khỏi memory storage
        del processing_jobs[process_id]
        
        # Ghi log thành công
        logger.info(f"Processing job {process_id} deleted")
        
        # Trả về thông báo thành công
        return {"message": "Processing job deleted successfully"}
        
    except Exception as e:
        # Ghi log lỗi và trả về HTTP error
        logger.error(f"Delete job error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/cad/jobs")
async def list_processing_jobs():
    """
    List all processing jobs endpoint - Liệt kê tất cả jobs đang xử lý
    
    Returns:
        dict: Danh sách tất cả jobs với thông tin cơ bản
        
    Raises:
        HTTPException: Nếu có lỗi
    """
    try:
        # Tạo danh sách thông tin jobs
        jobs_info = []
        for job_id, job in processing_jobs.items():
            jobs_info.append({
                "job_id": job_id,  # ID của job
                "file_id": job.file_id,  # ID của file gốc
                "status": job.status,  # Trạng thái hiện tại
                "progress": job.progress,  # Tiến độ (0-100)
                "created_at": job.created_at,  # Thời gian tạo
                "updated_at": job.updated_at  # Thời gian cập nhật cuối
            })
        
        # Trả về danh sách jobs và tổng số
        return {"jobs": jobs_info, "total": len(jobs_info)}
        
    except Exception as e:
        # Ghi log lỗi và trả về HTTP error
        logger.error(f"List jobs error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/cad/providers")
async def get_api_providers():
    """
    Get API providers status endpoint - Lấy trạng thái của tất cả API providers
    
    Returns:
        dict: Thông tin về các API providers (status, cost, features)
        
    Raises:
        HTTPException: Nếu có lỗi
    """
    try:
        # Import và khởi tạo External API Gateway
        from services.external_api_gateway import ExternalAPIGateway
        gateway = ExternalAPIGateway()
        
        # Lấy trạng thái của tất cả providers
        providers_status = gateway.get_provider_status()
        
        # Trả về thông tin providers
        return {
            "providers": providers_status,  # Trạng thái chi tiết từng provider
            "default_provider": "autodesk_forge",  # Provider mặc định
            "fallback_providers": ["sharecad", "cadviewer360", "cloudconvert"]  # Providers dự phòng
        }
        
    except Exception as e:
        # Ghi log lỗi và trả về HTTP error
        logger.error(f"Get providers error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/cad/providers/{provider}/test")
async def test_api_provider(provider: str):
    """
    Test API provider endpoint - Test một API provider cụ thể
    
    Args:
        provider (str): Tên provider cần test (autodesk_forge, sharecad, etc.)
        
    Returns:
        dict: Kết quả test (success/error, message, components_found)
        
    Raises:
        HTTPException: Nếu provider không hợp lệ hoặc có lỗi
    """
    try:
        # Import các class cần thiết
        from services.external_api_gateway import ExternalAPIGateway, APIProvider
        
        # Validate provider name
        try:
            provider_enum = APIProvider(provider)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid provider: {provider}")
        
        # Khởi tạo gateway
        gateway = ExternalAPIGateway()
        
        # Tạo mock file để test
        mock_file_content = b"mock_cad_content"
        mock_filename = "test.dwg"
        
        try:
            # Test provider với mock file
            components = await gateway.parse_cad_file(mock_file_content, mock_filename, provider_enum)
            
            # Trả về kết quả thành công
            return {
                "provider": provider,
                "status": "success",
                "message": f"Provider {provider} is working correctly",
                "components_found": len(components)
            }
        except Exception as test_error:
            # Trả về kết quả lỗi
            return {
                "provider": provider,
                "status": "error",
                "message": f"Provider {provider} test failed: {str(test_error)}"
            }
        
    except Exception as e:
        # Ghi log lỗi và trả về HTTP error
        logger.error(f"Test provider error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================
# Chạy ứng dụng khi file được execute trực tiếp
if __name__ == "__main__":
    import uvicorn  # ASGI server để chạy FastAPI
    
    # Chạy server với cấu hình
    uvicorn.run(
        app,  # FastAPI application
        host="0.0.0.0",  # Listen trên tất cả interfaces
        port=8000  # Port 8000
    )
