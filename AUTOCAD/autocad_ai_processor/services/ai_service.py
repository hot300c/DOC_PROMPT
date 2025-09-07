import numpy as np
import logging
from typing import Optional, Dict, Any
from models.schemas import Component, AIAnalysisResult, ComponentType, ShapeType, SizeCategory, PositionType

logger = logging.getLogger(__name__)


class AIService:
    def __init__(self):
        self._load_model()
    
    def _load_model(self):
        """Load AI model for component analysis"""
        try:
            # In a real implementation, you would load a pre-trained model
            # For now, we'll use a simple rule-based approach
            logger.info("AI Service initialized with rule-based analysis")
        except Exception as e:
            logger.error(f"Failed to load AI model: {e}")
            raise
    
    async def analyze_component(self, component: Component) -> AIAnalysisResult:
        """Phân tích component và trả về kết quả AI"""
        try:
            # Extract features from component
            features = self._extract_features(component)
            
            # Analyze component type
            component_type = self._analyze_component_type(features)
            
            # Analyze shape
            shape_type = self._analyze_shape_type(features)
            
            # Analyze size
            size_category = self._analyze_size_category(features)
            
            # Analyze position
            position = self._analyze_position(features)
            
            # Calculate confidence score
            confidence_score = self._calculate_confidence(features, component_type, shape_type)
            
            # Generate description
            description = self._generate_description(component_type, shape_type, size_category, position)
            
            return AIAnalysisResult(
                component_type=component_type,
                shape_type=shape_type,
                size_category=size_category,
                position=position,
                confidence_score=confidence_score,
                description=description
            )
            
        except Exception as e:
            logger.error(f"AI analysis failed for component {component.id}: {e}")
            # Return default analysis
            return self._get_default_analysis()
    
    def _extract_features(self, component: Component) -> Dict[str, Any]:
        """Trích xuất features từ component"""
        features = {
            "dimensions": component.dimensions or {},
            "metadata": component.metadata or {},
            "shape_type": component.shape_type,
            "size_category": component.size_category
        }
        
        # Extract geometric features
        if component.dimensions:
            features["volume"] = self._calculate_volume(component.dimensions)
            features["aspect_ratio"] = self._calculate_aspect_ratio(component.dimensions)
            features["surface_area"] = self._estimate_surface_area(component.dimensions)
        
        return features
    
    def _analyze_component_type(self, features: Dict[str, Any]) -> ComponentType:
        """Phân tích loại component dựa trên features"""
        dimensions = features.get("dimensions", {})
        metadata = features.get("metadata", {})
        
        # Rule-based analysis
        if "bearing" in str(metadata).lower() or "ball" in str(metadata).lower():
            return ComponentType.BEARING
        
        # Analyze based on dimensions and shape
        if features.get("shape_type") == ShapeType.CYLINDER:
            if dimensions.get("depth", 0) > dimensions.get("width", 0) * 2:
                return ComponentType.SHAFT
            else:
                return ComponentType.BEARING
        
        if features.get("shape_type") == ShapeType.SQUARE:
            if dimensions.get("depth", 0) < dimensions.get("width", 0) * 0.1:
                return ComponentType.WASHER
            else:
                return ComponentType.HOUSING
        
        # Analyze based on size
        size_category = features.get("size_category")
        if size_category == SizeCategory.SMALL:
            if features.get("shape_type") == ShapeType.CIRCLE:
                return ComponentType.BOLT
            else:
                return ComponentType.NUT
        
        # Default analysis
        return ComponentType.UNKNOWN
    
    def _analyze_shape_type(self, features: Dict[str, Any]) -> ShapeType:
        """Phân tích hình dạng component"""
        dimensions = features.get("dimensions", {})
        
        if not dimensions:
            return ShapeType.COMPLEX
        
        width = dimensions.get("width", 0)
        height = dimensions.get("height", 0)
        depth = dimensions.get("depth", 0)
        
        # Analyze shape based on dimensions
        if abs(width - height) < 0.1 and abs(height - depth) < 0.1:
            return ShapeType.SPHERE
        elif abs(width - height) < 0.1 and depth > width * 2:
            return ShapeType.CYLINDER
        elif abs(width - height) < 0.1 and depth < width * 0.1:
            return ShapeType.CIRCLE
        elif width > height * 2 and height > depth * 2:
            return ShapeType.RECTANGLE
        elif abs(width - height) < 0.1:
            return ShapeType.SQUARE
        else:
            return ShapeType.COMPLEX
    
    def _analyze_size_category(self, features: Dict[str, Any]) -> SizeCategory:
        """Phân tích kích thước component"""
        dimensions = features.get("dimensions", {})
        
        if not dimensions:
            return SizeCategory.MEDIUM
        
        max_dimension = max(dimensions.values()) if dimensions.values() else 1.0
        
        if max_dimension < 10:
            return SizeCategory.SMALL
        elif max_dimension < 100:
            return SizeCategory.MEDIUM
        else:
            return SizeCategory.LARGE
    
    def _analyze_position(self, features: Dict[str, Any]) -> PositionType:
        """Phân tích vị trí component"""
        # Simplified position analysis
        # In a real implementation, this would analyze spatial relationships
        return PositionType.CENTER
    
    def _calculate_confidence(self, features: Dict[str, Any], component_type: ComponentType, shape_type: ShapeType) -> float:
        """Tính toán confidence score"""
        confidence = 0.5  # Base confidence
        
        # Increase confidence based on feature quality
        if features.get("dimensions"):
            confidence += 0.2
        
        if features.get("metadata"):
            confidence += 0.1
        
        # Increase confidence for well-defined types
        if component_type != ComponentType.UNKNOWN:
            confidence += 0.2
        
        # Ensure confidence is between 0 and 1
        return min(1.0, max(0.0, confidence))
    
    def _generate_description(self, component_type: ComponentType, shape_type: ShapeType, 
                            size_category: SizeCategory, position: PositionType) -> str:
        """Tạo mô tả cho component"""
        description_parts = [
            f"{size_category.value} {component_type.value}",
            f"with {shape_type.value} shape",
            f"positioned at {position.value}"
        ]
        
        return " ".join(description_parts)
    
    def _calculate_volume(self, dimensions: Dict[str, float]) -> float:
        """Tính toán thể tích"""
        width = dimensions.get("width", 0)
        height = dimensions.get("height", 0)
        depth = dimensions.get("depth", 0)
        
        return width * height * depth
    
    def _calculate_aspect_ratio(self, dimensions: Dict[str, float]) -> float:
        """Tính toán tỷ lệ khung hình"""
        width = dimensions.get("width", 1)
        height = dimensions.get("height", 1)
        
        return max(width, height) / min(width, height)
    
    def _estimate_surface_area(self, dimensions: Dict[str, float]) -> float:
        """Ước tính diện tích bề mặt"""
        width = dimensions.get("width", 0)
        height = dimensions.get("height", 0)
        depth = dimensions.get("depth", 0)
        
        # Simplified surface area calculation for rectangular shapes
        return 2 * (width * height + width * depth + height * depth)
    
    def _get_default_analysis(self) -> AIAnalysisResult:
        """Trả về phân tích mặc định khi AI thất bại"""
        return AIAnalysisResult(
            component_type=ComponentType.UNKNOWN,
            shape_type=ShapeType.COMPLEX,
            size_category=SizeCategory.MEDIUM,
            position=PositionType.CENTER,
            confidence_score=0.0,
            description="Unknown component with complex shape"
        )
    
    async def batch_analyze_components(self, components: list[Component]) -> list[AIAnalysisResult]:
        """Phân tích nhiều components cùng lúc"""
        results = []
        
        for component in components:
            try:
                result = await self.analyze_component(component)
                results.append(result)
            except Exception as e:
                logger.error(f"Batch analysis failed for component {component.id}: {e}")
                results.append(self._get_default_analysis())
        
        return results
