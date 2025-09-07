import re
from typing import Dict, List
import logging
from models.schemas import AIAnalysisResult, ComponentType, ShapeType, SizeCategory, PositionType

logger = logging.getLogger(__name__)


class NameGenerator:
    def __init__(self):
        self.naming_rules = self._initialize_naming_rules()
        self.name_cache = {}  # Cache để tránh trùng tên
    
    def _initialize_naming_rules(self) -> Dict[str, Dict]:
        """Khởi tạo quy tắc đặt tên"""
        return {
            "component_type_mapping": {
                ComponentType.BEARING: "Bearing",
                ComponentType.SHAFT: "Shaft", 
                ComponentType.HOUSING: "Housing",
                ComponentType.GEAR: "Gear",
                ComponentType.BOLT: "Bolt",
                ComponentType.NUT: "Nut",
                ComponentType.WASHER: "Washer",
                ComponentType.SPRING: "Spring",
                ComponentType.UNKNOWN: "Component"
            },
            "shape_mapping": {
                ShapeType.CIRCLE: "Circle",
                ShapeType.SQUARE: "Square",
                ShapeType.TRIANGLE: "Triangle",
                ShapeType.RECTANGLE: "Rectangle",
                ShapeType.CYLINDER: "Cylinder",
                ShapeType.SPHERE: "Sphere",
                ShapeType.COMPLEX: "Complex"
            },
            "size_mapping": {
                SizeCategory.SMALL: "Small",
                SizeCategory.MEDIUM: "Medium",
                SizeCategory.LARGE: "Large"
            },
            "position_mapping": {
                PositionType.TOP: "Top",
                PositionType.BOTTOM: "Bottom",
                PositionType.LEFT: "Left",
                PositionType.RIGHT: "Right",
                PositionType.CENTER: "Center",
                PositionType.FRONT: "Front",
                PositionType.BACK: "Back"
            }
        }
    
    async def generate_name(self, analysis_result: AIAnalysisResult, index: int) -> str:
        """Tạo tên cho component dựa trên kết quả phân tích AI"""
        try:
            # Tạo tên theo format: [Function]_[Shape]_[Size]_[Position]_[Index]
            function_name = self._get_function_name(analysis_result.component_type)
            shape_name = self._get_shape_name(analysis_result.shape_type)
            size_name = self._get_size_name(analysis_result.size_category)
            position_name = self._get_position_name(analysis_result.position)
            
            # Tạo tên cơ bản
            base_name = f"{function_name}_{shape_name}_{size_name}_{position_name}"
            
            # Thêm index để tránh trùng
            final_name = f"{base_name}_{index+1:03d}"
            
            # Kiểm tra và đảm bảo tên unique
            final_name = self._ensure_unique_name(final_name)
            
            # Cache tên đã sử dụng
            self.name_cache[final_name] = True
            
            logger.info(f"Generated name: {final_name} for analysis: {analysis_result.description}")
            
            return final_name
            
        except Exception as e:
            logger.error(f"Name generation failed: {e}")
            # Fallback name
            return f"Component_{index+1:03d}"
    
    def _get_function_name(self, component_type: ComponentType) -> str:
        """Lấy tên chức năng từ component type"""
        return self.naming_rules["component_type_mapping"].get(
            component_type, "Component"
        )
    
    def _get_shape_name(self, shape_type: ShapeType) -> str:
        """Lấy tên hình dạng"""
        return self.naming_rules["shape_mapping"].get(
            shape_type, "Complex"
        )
    
    def _get_size_name(self, size_category: SizeCategory) -> str:
        """Lấy tên kích thước"""
        return self.naming_rules["size_mapping"].get(
            size_category, "Medium"
        )
    
    def _get_position_name(self, position: PositionType) -> str:
        """Lấy tên vị trí"""
        return self.naming_rules["position_mapping"].get(
            position, "Center"
        )
    
    def _ensure_unique_name(self, name: str) -> str:
        """Đảm bảo tên là unique"""
        if name not in self.name_cache:
            return name
        
        # Nếu tên đã tồn tại, thêm suffix
        counter = 1
        while f"{name}_{counter}" in self.name_cache:
            counter += 1
        
        return f"{name}_{counter}"
    
    def generate_simple_name(self, component_type: ComponentType, index: int) -> str:
        """Tạo tên đơn giản khi AI analysis thất bại"""
        function_name = self._get_function_name(component_type)
        return f"{function_name}_{index+1:03d}"
    
    def generate_custom_name(self, prefix: str, index: int, suffix: str = "") -> str:
        """Tạo tên tùy chỉnh"""
        name = f"{prefix}_{index+1:03d}"
        if suffix:
            name += f"_{suffix}"
        
        return self._ensure_unique_name(name)
    
    def validate_name(self, name: str) -> bool:
        """Validate tên component"""
        if not name or len(name.strip()) == 0:
            return False
        
        # Kiểm tra ký tự không hợp lệ
        if not re.match(r'^[A-Za-z0-9_]+$', name):
            return False
        
        # Kiểm tra độ dài
        if len(name) > 100:
            return False
        
        return True
    
    def sanitize_name(self, name: str) -> str:
        """Làm sạch tên component"""
        # Loại bỏ ký tự không hợp lệ
        sanitized = re.sub(r'[^A-Za-z0-9_]', '_', name)
        
        # Loại bỏ underscore liên tiếp
        sanitized = re.sub(r'_+', '_', sanitized)
        
        # Loại bỏ underscore ở đầu và cuối
        sanitized = sanitized.strip('_')
        
        # Đảm bảo tên không rỗng
        if not sanitized:
            sanitized = "Component"
        
        return sanitized
    
    def get_naming_statistics(self) -> Dict[str, int]:
        """Lấy thống kê về việc đặt tên"""
        stats = {
            "total_names_generated": len(self.name_cache),
            "unique_names": len(set(self.name_cache.keys()))
        }
        
        # Thống kê theo prefix
        prefix_stats = {}
        for name in self.name_cache.keys():
            prefix = name.split('_')[0] if '_' in name else name
            prefix_stats[prefix] = prefix_stats.get(prefix, 0) + 1
        
        stats["prefix_statistics"] = prefix_stats
        
        return stats
    
    def clear_cache(self):
        """Xóa cache tên"""
        self.name_cache.clear()
        logger.info("Name cache cleared")
    
    def export_naming_rules(self) -> Dict:
        """Export quy tắc đặt tên"""
        return self.naming_rules.copy()
    
    def import_naming_rules(self, rules: Dict):
        """Import quy tắc đặt tên"""
        self.naming_rules.update(rules)
        logger.info("Naming rules updated")
