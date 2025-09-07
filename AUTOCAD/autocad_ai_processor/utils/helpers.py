import uuid
import hashlib
import os
from datetime import datetime
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


def generate_unique_id() -> str:
    """Generate unique ID"""
    return str(uuid.uuid4())


def generate_file_hash(file_content: bytes) -> str:
    """Generate hash for file content"""
    return hashlib.md5(file_content).hexdigest()


def get_file_size_mb(file_size_bytes: int) -> float:
    """Convert bytes to MB"""
    return file_size_bytes / (1024 * 1024)


def format_file_size(file_size_bytes: int) -> str:
    """Format file size in human readable format"""
    if file_size_bytes < 1024:
        return f"{file_size_bytes} B"
    elif file_size_bytes < 1024 * 1024:
        return f"{file_size_bytes / 1024:.1f} KB"
    elif file_size_bytes < 1024 * 1024 * 1024:
        return f"{file_size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{file_size_bytes / (1024 * 1024 * 1024):.1f} GB"


def get_timestamp() -> str:
    """Get current timestamp in ISO format"""
    return datetime.now().isoformat()


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage"""
    # Remove or replace unsafe characters
    unsafe_chars = '<>:"/\\|?*'
    for char in unsafe_chars:
        filename = filename.replace(char, '_')
    
    # Remove leading/trailing spaces and dots
    filename = filename.strip(' .')
    
    # Ensure filename is not empty
    if not filename:
        filename = "unnamed_file"
    
    return filename


def ensure_directory_exists(directory_path: str) -> bool:
    """Ensure directory exists, create if not"""
    try:
        os.makedirs(directory_path, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Failed to create directory {directory_path}: {e}")
        return False


def get_file_extension(filename: str) -> str:
    """Get file extension from filename"""
    return os.path.splitext(filename)[1].lower()


def is_supported_file_type(filename: str) -> bool:
    """Check if file type is supported"""
    supported_extensions = ['.dwg', '.dxf', '.stl', '.obj', '.ply']
    extension = get_file_extension(filename)
    return extension in supported_extensions


def calculate_processing_time(start_time: datetime, end_time: datetime) -> float:
    """Calculate processing time in seconds"""
    return (end_time - start_time).total_seconds()


def format_processing_time(seconds: float) -> str:
    """Format processing time in human readable format"""
    if seconds < 60:
        return f"{seconds:.1f} seconds"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f} minutes"
    else:
        hours = seconds / 3600
        return f"{hours:.1f} hours"


def create_progress_message(current: int, total: int, operation: str) -> str:
    """Create progress message"""
    percentage = (current / total) * 100 if total > 0 else 0
    return f"{operation}: {current}/{total} ({percentage:.1f}%)"


def validate_dimensions(dimensions: Dict[str, float]) -> bool:
    """Validate component dimensions"""
    if not dimensions:
        return False
    
    required_keys = ['width', 'height', 'depth']
    for key in required_keys:
        if key not in dimensions:
            return False
        if dimensions[key] <= 0:
            return False
    
    return True


def normalize_dimensions(dimensions: Dict[str, float]) -> Dict[str, float]:
    """Normalize dimensions to positive values"""
    normalized = {}
    for key, value in dimensions.items():
        normalized[key] = abs(float(value)) if value is not None else 0.0
    return normalized


def calculate_component_volume(dimensions: Dict[str, float]) -> float:
    """Calculate component volume"""
    if not validate_dimensions(dimensions):
        return 0.0
    
    return dimensions['width'] * dimensions['height'] * dimensions['depth']


def calculate_component_surface_area(dimensions: Dict[str, float]) -> float:
    """Calculate component surface area (for rectangular shapes)"""
    if not validate_dimensions(dimensions):
        return 0.0
    
    w, h, d = dimensions['width'], dimensions['height'], dimensions['depth']
    return 2 * (w * h + w * d + h * d)


def get_component_complexity_score(dimensions: Dict[str, float], metadata: Dict[str, Any]) -> float:
    """Calculate component complexity score (0-1)"""
    score = 0.0
    
    # Volume factor
    volume = calculate_component_volume(dimensions)
    if volume > 0:
        # Normalize volume (assuming max reasonable volume is 1000000)
        volume_score = min(1.0, volume / 1000000)
        score += volume_score * 0.3
    
    # Aspect ratio factor
    if validate_dimensions(dimensions):
        w, h, d = dimensions['width'], dimensions['height'], dimensions['depth']
        max_dim = max(w, h, d)
        min_dim = min(w, h, d)
        if min_dim > 0:
            aspect_ratio = max_dim / min_dim
            aspect_score = min(1.0, aspect_ratio / 10)  # Normalize to 0-1
            score += aspect_score * 0.2
    
    # Metadata complexity
    if metadata:
        metadata_score = min(1.0, len(str(metadata)) / 1000)  # Normalize to 0-1
        score += metadata_score * 0.2
    
    # Shape complexity (simplified)
    score += 0.3  # Base complexity
    
    return min(1.0, score)


def create_error_response(error_message: str, error_code: str = "UNKNOWN_ERROR") -> Dict[str, Any]:
    """Create standardized error response"""
    return {
        "error": True,
        "error_code": error_code,
        "error_message": error_message,
        "timestamp": get_timestamp()
    }


def create_success_response(data: Any, message: str = "Success") -> Dict[str, Any]:
    """Create standardized success response"""
    return {
        "success": True,
        "message": message,
        "data": data,
        "timestamp": get_timestamp()
    }
