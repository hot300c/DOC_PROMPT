# =============================================================================
# DATA MODELS & SCHEMAS
# =============================================================================
# File này định nghĩa tất cả các data structures (models) được sử dụng trong ứng dụng
# Sử dụng Pydantic để validation và serialization

from pydantic import BaseModel, Field  # Pydantic cho data validation
from typing import List, Optional, Dict, Any  # Type hints
from enum import Enum  # Enum cho các giá trị cố định


# =============================================================================
# ENUMS - Các giá trị cố định
# =============================================================================

class ProcessingStatus(str, Enum):
    """
    Trạng thái xử lý của một job
    """
    PENDING = "pending"      # Chờ xử lý
    PROCESSING = "processing"  # Đang xử lý
    COMPLETED = "completed"   # Hoàn thành
    FAILED = "failed"        # Thất bại


class ComponentType(str, Enum):
    """
    Loại component trong file AutoCAD
    """
    BEARING = "bearing"    # Vòng bi
    SHAFT = "shaft"        # Trục
    HOUSING = "housing"    # Vỏ
    GEAR = "gear"          # Bánh răng
    BOLT = "bolt"          # Bu lông
    NUT = "nut"            # Đai ốc
    WASHER = "washer"      # Vòng đệm
    SPRING = "spring"      # Lò xo
    UNKNOWN = "unknown"    # Không xác định


class ShapeType(str, Enum):
    """
    Hình dạng của component
    """
    CIRCLE = "circle"      # Hình tròn
    SQUARE = "square"      # Hình vuông
    TRIANGLE = "triangle"  # Hình tam giác
    RECTANGLE = "rectangle"  # Hình chữ nhật
    CYLINDER = "cylinder"  # Hình trụ
    SPHERE = "sphere"      # Hình cầu
    COMPLEX = "complex"    # Hình phức tạp


class SizeCategory(str, Enum):
    """
    Phân loại kích thước component
    """
    SMALL = "small"        # Nhỏ
    MEDIUM = "medium"      # Trung bình
    LARGE = "large"        # Lớn


class PositionType(str, Enum):
    """
    Vị trí của component
    """
    TOP = "top"            # Trên
    BOTTOM = "bottom"      # Dưới
    LEFT = "left"          # Trái
    RIGHT = "right"        # Phải
    CENTER = "center"      # Giữa
    FRONT = "front"        # Trước
    BACK = "back"          # Sau


# =============================================================================
# DATA MODELS - Các cấu trúc dữ liệu chính
# =============================================================================

class Component(BaseModel):
    """
    Model cho một component trong file AutoCAD
    
    Attributes:
        id (str): ID duy nhất của component
        name (Optional[str]): Tên component (có thể được AI tạo)
        original_name (Optional[str]): Tên gốc từ file AutoCAD
        component_type (Optional[ComponentType]): Loại component (bearing, shaft, etc.)
        shape_type (Optional[ShapeType]): Hình dạng (circle, square, etc.)
        size_category (Optional[SizeCategory]): Kích thước (small, medium, large)
        position (Optional[PositionType]): Vị trí (top, bottom, center, etc.)
        dimensions (Optional[Dict[str, float]]): Kích thước chi tiết (width, height, depth)
        metadata (Optional[Dict[str, Any]]): Thông tin bổ sung
        has_navigator (bool): Có tên sẵn trong file AutoCAD không
        confidence_score (Optional[float]): Độ tin cậy của AI analysis (0-1)
    """
    id: str  # ID duy nhất
    name: Optional[str] = None  # Tên component
    original_name: Optional[str] = None  # Tên gốc
    component_type: Optional[ComponentType] = None  # Loại component
    shape_type: Optional[ShapeType] = None  # Hình dạng
    size_category: Optional[SizeCategory] = None  # Kích thước
    position: Optional[PositionType] = None  # Vị trí
    dimensions: Optional[Dict[str, float]] = None  # Kích thước chi tiết
    metadata: Optional[Dict[str, Any]] = None  # Metadata bổ sung
    has_navigator: bool = False  # Có tên sẵn không
    confidence_score: Optional[float] = None  # Độ tin cậy AI


class CADFile(BaseModel):
    """
    Model cho file AutoCAD đã upload
    
    Attributes:
        file_id (str): ID duy nhất của file
        filename (str): Tên file gốc
        file_size (int): Kích thước file (bytes)
        upload_time (str): Thời gian upload (ISO format)
        status (ProcessingStatus): Trạng thái xử lý
        file_path (str): Đường dẫn file trên server
    """
    file_id: str  # ID duy nhất
    filename: str  # Tên file
    file_size: int  # Kích thước file
    upload_time: str  # Thời gian upload
    status: ProcessingStatus  # Trạng thái
    file_path: str  # Đường dẫn file


class ProcessingJob(BaseModel):
    """
    Model cho một job xử lý file AutoCAD
    
    Attributes:
        job_id (str): ID duy nhất của job
        file_id (str): ID của file được xử lý
        status (ProcessingStatus): Trạng thái hiện tại
        progress (int): Tiến độ xử lý (0-100)
        message (str): Thông báo hiện tại
        created_at (str): Thời gian tạo job
        updated_at (str): Thời gian cập nhật cuối
        components (List[Component]): Danh sách components đã xử lý
        output_files (List[str]): Danh sách file output
    """
    job_id: str  # ID duy nhất
    file_id: str  # ID file
    status: ProcessingStatus  # Trạng thái
    progress: int = 0  # Tiến độ (0-100)
    message: str = ""  # Thông báo
    created_at: str  # Thời gian tạo
    updated_at: str  # Thời gian cập nhật
    components: List[Component] = []  # Components đã xử lý
    output_files: List[str] = []  # File output


# =============================================================================
# API RESPONSE MODELS - Các model cho API responses
# =============================================================================

class UploadResponse(BaseModel):
    """
    Response model cho API upload file
    
    Attributes:
        file_id (str): ID của file đã upload
        status (str): Trạng thái upload (success/error)
        message (str): Thông báo
    """
    file_id: str  # ID file
    status: str  # Trạng thái
    message: str  # Thông báo


class ProcessResponse(BaseModel):
    """
    Response model cho API start processing
    
    Attributes:
        process_id (str): ID của job xử lý
        status (str): Trạng thái (started/error)
        message (str): Thông báo
    """
    process_id: str  # ID job
    status: str  # Trạng thái
    message: str  # Thông báo


class StatusResponse(BaseModel):
    """
    Response model cho API get processing status
    
    Attributes:
        status (ProcessingStatus): Trạng thái hiện tại
        progress (int): Tiến độ (0-100)
        message (str): Thông báo hiện tại
        components_count (Optional[int]): Số components đã xử lý
    """
    status: ProcessingStatus  # Trạng thái
    progress: int  # Tiến độ
    message: str  # Thông báo
    components_count: Optional[int] = None  # Số components


class DownloadResponse(BaseModel):
    """
    Response model cho API download results
    
    Attributes:
        download_urls (List[str]): Danh sách URLs để download
        files (List[Dict[str, str]]): Thông tin chi tiết về files
    """
    download_urls: List[str]  # URLs download
    files: List[Dict[str, str]]  # Thông tin files


# =============================================================================
# AI MODELS - Các model cho AI processing
# =============================================================================

class AIAnalysisResult(BaseModel):
    """
    Kết quả phân tích AI cho một component
    
    Attributes:
        component_type (ComponentType): Loại component được nhận dạng
        shape_type (ShapeType): Hình dạng được nhận dạng
        size_category (SizeCategory): Kích thước được phân loại
        position (PositionType): Vị trí được xác định
        confidence_score (float): Độ tin cậy của phân tích (0-1)
        description (str): Mô tả chi tiết
    """
    component_type: ComponentType  # Loại component
    shape_type: ShapeType  # Hình dạng
    size_category: SizeCategory  # Kích thước
    position: PositionType  # Vị trí
    confidence_score: float  # Độ tin cậy
    description: str  # Mô tả


class NameGenerationRequest(BaseModel):
    """
    Request model cho việc tạo tên component
    
    Attributes:
        analysis_result (AIAnalysisResult): Kết quả phân tích AI
        index (int): Index của component trong danh sách
    """
    analysis_result: AIAnalysisResult  # Kết quả AI
    index: int  # Index component


class NameGenerationResponse(BaseModel):
    """
    Response model cho việc tạo tên component
    
    Attributes:
        generated_name (str): Tên được tạo
        confidence (float): Độ tin cậy của tên (0-1)
    """
    generated_name: str  # Tên được tạo
    confidence: float  # Độ tin cậy
