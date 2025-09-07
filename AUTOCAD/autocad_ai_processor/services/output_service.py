import ezdxf
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Tuple
import logging
from PIL import Image, ImageDraw, ImageFont
import io
from models.schemas import Component
from services.external_api_gateway import ExternalAPIGateway, APIProvider

logger = logging.getLogger(__name__)


class OutputService:
    def __init__(self, output_dir: str = "outputs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.external_api_gateway = ExternalAPIGateway()
        self.use_external_api = True  # Flag to enable/disable external API usage
    
    async def create_2d_files(self, components: List[Component], job_id: str, use_external_api: bool = True) -> List[bytes]:
        """Tạo các file 2D từ components"""
        try:
            files = []
            
            # Try external API first for 2D view creation
            if use_external_api:
                try:
                    external_files = await self._create_2d_with_external_api(components, job_id)
                    files.extend(external_files)
                    logger.info(f"Created {len(external_files)} files using external API")
                except Exception as e:
                    logger.warning(f"External API 2D creation failed, falling back to local: {e}")
                    # Fall back to local creation
            
            # If external API failed or not used, create locally
            if not files or not use_external_api:
                local_files = await self._create_2d_locally(components, job_id)
                files.extend(local_files)
                logger.info(f"Created {len(local_files)} files using local processing")
            
            # Post-process files to add component names
            processed_files = []
            for filename, file_content in files:
                processed_content = await self._add_component_names_to_file(file_content, components, filename)
                processed_files.append((filename, processed_content))
            
            logger.info(f"Created {len(processed_files)} output files for job {job_id}")
            return processed_files
            
        except Exception as e:
            logger.error(f"Error creating 2D files: {e}")
            raise
    
    async def _create_2d_with_external_api(self, components: List[Component], job_id: str) -> List[Tuple[str, bytes]]:
        """Create 2D files using external API"""
        try:
            # Use external API to create 2D views
            external_files = await self.external_api_gateway.create_2d_views(
                components,
                provider=APIProvider.AUTODESK_FORGE  # Use Forge as primary
            )
            
            # Convert external API results to our format
            files = []
            view_types = ["top", "front", "side", "isometric"]
            
            for i, file_content in enumerate(external_files):
                if i < len(view_types):
                    filename = f"{view_types[i]}_view.dxf"
                else:
                    filename = f"view_{i+1}.dxf"
                
                files.append((filename, file_content))
            
            return files
            
        except Exception as e:
            logger.error(f"External API 2D creation failed: {e}")
            raise
    
    async def _create_2d_locally(self, components: List[Component], job_id: str) -> List[Tuple[str, bytes]]:
        """Create 2D files using local processing"""
        try:
            # Tạo các view khác nhau
            top_view = await self._create_top_view(components)
            front_view = await self._create_front_view(components)
            side_view = await self._create_side_view(components)
            isometric_view = await self._create_isometric_view(components)
            
            # Tạo file DXF cho mỗi view
            files = []
            
            # Top view DXF
            top_dxf = await self._create_dxf_file(components, "top", top_view)
            files.append(("top_view.dxf", top_dxf))
            
            # Front view DXF
            front_dxf = await self._create_dxf_file(components, "front", front_view)
            files.append(("front_view.dxf", front_dxf))
            
            # Side view DXF
            side_dxf = await self._create_dxf_file(components, "side", side_view)
            files.append(("side_view.dxf", side_dxf))
            
            # Isometric view DXF
            iso_dxf = await self._create_dxf_file(components, "isometric", isometric_view)
            files.append(("isometric_view.dxf", iso_dxf))
            
            # Tạo file tổng hợp
            combined_dxf = await self._create_combined_dxf(components)
            files.append(("combined_view.dxf", combined_dxf))
            
            # Tạo file PDF (nếu cần)
            pdf_file = await self._create_pdf_file(components, job_id)
            if pdf_file:
                files.append(("technical_drawing.pdf", pdf_file))
            
            return files
            
        except Exception as e:
            logger.error(f"Local 2D creation failed: {e}")
            raise
    
    async def _add_component_names_to_file(self, file_content: bytes, components: List[Component], filename: str) -> bytes:
        """Add component names to the file content"""
        try:
            # This method would add component names to the DXF file
            # For now, we'll return the content as-is
            # In a real implementation, you would:
            # 1. Parse the DXF file
            # 2. Add text entities with component names
            # 3. Save the modified DXF file
            
            return file_content
            
        except Exception as e:
            logger.error(f"Error adding component names to {filename}: {e}")
            return file_content
    
    async def _create_top_view(self, components: List[Component]) -> Dict[str, Any]:
        """Tạo top view của components"""
        view_data = {
            "view_type": "top",
            "components": [],
            "dimensions": {"width": 0, "height": 0}
        }
        
        for component in components:
            if component.dimensions:
                # Project 3D to 2D top view
                top_component = {
                    "id": component.id,
                    "name": component.name,
                    "x": 0,  # Simplified positioning
                    "y": 0,
                    "width": component.dimensions.get("width", 10),
                    "height": component.dimensions.get("height", 10),
                    "shape": component.shape_type.value if component.shape_type else "complex"
                }
                view_data["components"].append(top_component)
        
        return view_data
    
    async def _create_front_view(self, components: List[Component]) -> Dict[str, Any]:
        """Tạo front view của components"""
        view_data = {
            "view_type": "front",
            "components": [],
            "dimensions": {"width": 0, "height": 0}
        }
        
        for component in components:
            if component.dimensions:
                # Project 3D to 2D front view
                front_component = {
                    "id": component.id,
                    "name": component.name,
                    "x": 0,
                    "y": 0,
                    "width": component.dimensions.get("width", 10),
                    "height": component.dimensions.get("depth", 10),
                    "shape": component.shape_type.value if component.shape_type else "complex"
                }
                view_data["components"].append(front_component)
        
        return view_data
    
    async def _create_side_view(self, components: List[Component]) -> Dict[str, Any]:
        """Tạo side view của components"""
        view_data = {
            "view_type": "side",
            "components": [],
            "dimensions": {"width": 0, "height": 0}
        }
        
        for component in components:
            if component.dimensions:
                # Project 3D to 2D side view
                side_component = {
                    "id": component.id,
                    "name": component.name,
                    "x": 0,
                    "y": 0,
                    "width": component.dimensions.get("height", 10),
                    "height": component.dimensions.get("depth", 10),
                    "shape": component.shape_type.value if component.shape_type else "complex"
                }
                view_data["components"].append(side_component)
        
        return view_data
    
    async def _create_isometric_view(self, components: List[Component]) -> Dict[str, Any]:
        """Tạo isometric view của components"""
        view_data = {
            "view_type": "isometric",
            "components": [],
            "dimensions": {"width": 0, "height": 0}
        }
        
        for component in components:
            if component.dimensions:
                # Create isometric projection
                iso_component = {
                    "id": component.id,
                    "name": component.name,
                    "x": 0,
                    "y": 0,
                    "z": 0,
                    "width": component.dimensions.get("width", 10),
                    "height": component.dimensions.get("height", 10),
                    "depth": component.dimensions.get("depth", 10),
                    "shape": component.shape_type.value if component.shape_type else "complex"
                }
                view_data["components"].append(iso_component)
        
        return view_data
    
    async def _create_dxf_file(self, components: List[Component], view_type: str, view_data: Dict[str, Any]) -> bytes:
        """Tạo file DXF cho một view"""
        try:
            # Tạo DXF document
            doc = ezdxf.new('R2010')
            msp = doc.modelspace()
            
            # Thêm title block
            self._add_title_block(doc, view_type, len(components))
            
            # Vẽ các components
            for component_data in view_data["components"]:
                await self._draw_component(msp, component_data, view_type)
            
            # Lưu vào bytes
            output = io.BytesIO()
            doc.save(output)
            output.seek(0)
            
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"Error creating DXF file for {view_type}: {e}")
            raise
    
    async def _create_combined_dxf(self, components: List[Component]) -> bytes:
        """Tạo file DXF tổng hợp tất cả views"""
        try:
            doc = ezdxf.new('R2010')
            msp = doc.modelspace()
            
            # Thêm title block
            self._add_title_block(doc, "combined", len(components))
            
            # Tạo layout cho các views
            views = [
                ("top", 0, 0),
                ("front", 200, 0),
                ("side", 400, 0),
                ("isometric", 600, 0)
            ]
            
            for view_name, x_offset, y_offset in views:
                # Thêm view label
                msp.add_text(f"{view_name.upper()} VIEW", dxfattribs={'height': 5}).set_pos((x_offset, y_offset - 20))
                
                # Vẽ components cho view này
                view_data = await self._get_view_data(components, view_name)
                for component_data in view_data["components"]:
                    # Offset position
                    component_data["x"] += x_offset
                    component_data["y"] += y_offset
                    await self._draw_component(msp, component_data, view_name)
            
            # Lưu vào bytes
            output = io.BytesIO()
            doc.save(output)
            output.seek(0)
            
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"Error creating combined DXF: {e}")
            raise
    
    async def _get_view_data(self, components: List[Component], view_type: str) -> Dict[str, Any]:
        """Lấy dữ liệu view cho loại view cụ thể"""
        if view_type == "top":
            return await self._create_top_view(components)
        elif view_type == "front":
            return await self._create_front_view(components)
        elif view_type == "side":
            return await self._create_side_view(components)
        elif view_type == "isometric":
            return await self._create_isometric_view(components)
        else:
            return {"view_type": view_type, "components": [], "dimensions": {"width": 0, "height": 0}}
    
    async def _draw_component(self, msp, component_data: Dict[str, Any], view_type: str):
        """Vẽ component trong DXF"""
        try:
            x = component_data.get("x", 0)
            y = component_data.get("y", 0)
            width = component_data.get("width", 10)
            height = component_data.get("height", 10)
            name = component_data.get("name", "Unknown")
            shape = component_data.get("shape", "complex")
            
            # Vẽ hình dạng dựa trên shape type
            if shape in ["circle", "sphere"]:
                radius = min(width, height) / 2
                msp.add_circle((x + width/2, y + height/2), radius)
            elif shape in ["square", "rectangle"]:
                msp.add_lwpolyline([(x, y), (x + width, y), (x + width, y + height), (x, y + height), (x, y)])
            else:
                # Default: vẽ rectangle
                msp.add_lwpolyline([(x, y), (x + width, y), (x + width, y + height), (x, y + height), (x, y)])
            
            # Thêm tên component
            msp.add_text(name, dxfattribs={'height': 2}).set_pos((x, y - 5))
            
            # Thêm dimensions
            msp.add_text(f"{width:.1f}x{height:.1f}", dxfattribs={'height': 1.5}).set_pos((x, y - 8))
            
        except Exception as e:
            logger.error(f"Error drawing component {component_data.get('name', 'Unknown')}: {e}")
    
    def _add_title_block(self, doc, view_type: str, component_count: int):
        """Thêm title block vào DXF"""
        try:
            msp = doc.modelspace()
            
            # Title
            msp.add_text(f"AUTOCAD 3D TO 2D CONVERSION", dxfattribs={'height': 8}).set_pos((50, 280))
            msp.add_text(f"View: {view_type.upper()}", dxfattribs={'height': 5}).set_pos((50, 270))
            msp.add_text(f"Components: {component_count}", dxfattribs={'height': 4}).set_pos((50, 260))
            msp.add_text(f"Generated by AI Processing System", dxfattribs={'height': 3}).set_pos((50, 250))
            
        except Exception as e:
            logger.error(f"Error adding title block: {e}")
    
    async def _create_pdf_file(self, components: List[Component], job_id: str) -> bytes:
        """Tạo file PDF (placeholder - cần thêm thư viện PDF)"""
        # Trong thực tế, bạn sẽ sử dụng thư viện như reportlab hoặc weasyprint
        # Để tạo PDF từ DXF hoặc trực tiếp từ components
        logger.info(f"PDF generation not implemented yet for job {job_id}")
        return None
    
    def get_output_summary(self, components: List[Component]) -> Dict[str, Any]:
        """Tạo summary của output"""
        return {
            "total_components": len(components),
            "named_components": sum(1 for c in components if c.name),
            "views_created": ["top", "front", "side", "isometric", "combined"],
            "file_formats": ["dxf", "pdf"],
            "total_dimensions": sum(
                (c.dimensions.get("width", 0) * c.dimensions.get("height", 0) * c.dimensions.get("depth", 0))
                for c in components if c.dimensions
            )
        }
