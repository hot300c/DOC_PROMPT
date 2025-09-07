import asyncio
from typing import List, Optional
import logging
from models.schemas import Component, ComponentType, ProcessingStatus
from services.ai_service import AIService
from services.name_generator import NameGenerator

logger = logging.getLogger(__name__)


class ComponentAnalyzer:
    def __init__(self):
        self.ai_service = AIService()
        self.name_generator = NameGenerator()
    
    async def analyze_components(self, components: List[Component]) -> List[Component]:
        """Phân tích từng component và xử lý tên"""
        processed_components = []
        
        for i, component in enumerate(components):
            try:
                processed_component = await self._analyze_single_component(component, i)
                processed_components.append(processed_component)
                
                # Log progress
                logger.info(f"Processed component {i+1}/{len(components)}: {processed_component.name}")
                
            except Exception as e:
                logger.error(f"Error processing component {component.id}: {e}")
                # Keep original component if processing fails
                processed_components.append(component)
        
        return processed_components
    
    async def _analyze_single_component(self, component: Component, index: int) -> Component:
        """Phân tích một component"""
        # Kiểm tra có navigator/name không
        if component.has_navigator and component.original_name:
            # Sử dụng tên có sẵn
            component.name = component.original_name
            component.confidence_score = 1.0
            logger.info(f"Using existing name for component {component.id}: {component.name}")
            
        else:
            # Không có tên, sử dụng AI để tạo tên
            try:
                # Gửi component cho AI service để phân tích
                ai_analysis = await self.ai_service.analyze_component(component)
                
                # Tạo tên dựa trên kết quả AI
                generated_name = await self.name_generator.generate_name(
                    ai_analysis, index
                )
                
                # Cập nhật component với thông tin từ AI
                component.name = generated_name
                component.component_type = ai_analysis.component_type
                component.shape_type = ai_analysis.shape_type
                component.size_category = ai_analysis.size_category
                component.position = ai_analysis.position
                component.confidence_score = ai_analysis.confidence_score
                
                logger.info(f"Generated name for component {component.id}: {component.name}")
                
            except Exception as e:
                logger.error(f"AI analysis failed for component {component.id}: {e}")
                # Fallback: tạo tên đơn giản
                component.name = f"Component_{index+1:03d}"
                component.confidence_score = 0.0
        
        return component
    
    async def batch_analyze_components(self, components: List[Component], batch_size: int = 5) -> List[Component]:
        """Phân tích components theo batch để tối ưu performance"""
        processed_components = []
        
        for i in range(0, len(components), batch_size):
            batch = components[i:i + batch_size]
            
            # Xử lý batch song song
            tasks = []
            for j, component in enumerate(batch):
                task = self._analyze_single_component(component, i + j)
                tasks.append(task)
            
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Xử lý kết quả
            for result in batch_results:
                if isinstance(result, Exception):
                    logger.error(f"Batch processing error: {result}")
                    # Add original component if processing failed
                    processed_components.append(components[len(processed_components)])
                else:
                    processed_components.append(result)
            
            logger.info(f"Processed batch {i//batch_size + 1}/{(len(components) + batch_size - 1)//batch_size}")
        
        return processed_components
    
    def validate_component(self, component: Component) -> bool:
        """Validate component data"""
        if not component.id:
            return False
        
        if not component.name:
            return False
        
        if component.confidence_score is not None and (component.confidence_score < 0 or component.confidence_score > 1):
            return False
        
        return True
    
    def get_analysis_summary(self, components: List[Component]) -> dict:
        """Tạo summary của quá trình phân tích"""
        total_components = len(components)
        named_components = sum(1 for c in components if c.has_navigator)
        ai_generated_components = sum(1 for c in components if not c.has_navigator and c.name)
        
        # Thống kê theo loại component
        type_stats = {}
        for component in components:
            if component.component_type:
                type_stats[component.component_type.value] = type_stats.get(component.component_type.value, 0) + 1
        
        # Thống kê theo hình dạng
        shape_stats = {}
        for component in components:
            if component.shape_type:
                shape_stats[component.shape_type.value] = shape_stats.get(component.shape_type.value, 0) + 1
        
        # Thống kê confidence score
        confidence_scores = [c.confidence_score for c in components if c.confidence_score is not None]
        avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
        
        return {
            "total_components": total_components,
            "named_components": named_components,
            "ai_generated_components": ai_generated_components,
            "type_statistics": type_stats,
            "shape_statistics": shape_stats,
            "average_confidence": avg_confidence,
            "processing_success_rate": (named_components + ai_generated_components) / total_components if total_components > 0 else 0
        }
