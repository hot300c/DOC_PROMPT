import ezdxf
import trimesh
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging
from models.schemas import Component, ComponentType, ShapeType, SizeCategory, PositionType
from services.external_api_gateway import ExternalAPIGateway, APIProvider

logger = logging.getLogger(__name__)


class CADParser:
    def __init__(self):
        self.supported_formats = ['.dwg', '.dxf', '.stl', '.obj', '.ply']
        self.external_api_gateway = ExternalAPIGateway()
        self.use_external_api = True  # Flag to enable/disable external API usage
    
    async def parse_file(self, file_path: str, use_external_api: bool = True) -> List[Component]:
        """Parse file CAD và trích xuất các components"""
        file_path = Path(file_path)
        file_extension = file_path.suffix.lower()
        
        # For complex AutoCAD files, use external API
        if use_external_api and file_extension in ['.dwg', '.dxf']:
            try:
                return await self._parse_with_external_api(file_path)
            except Exception as e:
                logger.warning(f"External API parsing failed, falling back to local parsing: {e}")
                # Fall back to local parsing
        
        # Local parsing for simple files or when external API fails
        if file_extension in ['.dwg', '.dxf']:
            return await self._parse_dxf_file(file_path)
        elif file_extension in ['.stl', '.obj', '.ply']:
            return await self._parse_3d_file(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    
    async def _parse_with_external_api(self, file_path: Path) -> List[Component]:
        """Parse file using external API"""
        try:
            # Read file content
            with open(file_path, 'rb') as f:
                file_content = f.read()
            
            # Use external API to parse the file
            components = await self.external_api_gateway.parse_cad_file(
                file_content, 
                file_path.name,
                provider=APIProvider.AUTODESK_FORGE  # Use Forge as primary
            )
            
            # Convert external API components to internal format
            internal_components = []
            for component in components:
                internal_component = self._convert_external_component(component)
                internal_components.append(internal_component)
            
            logger.info(f"Successfully parsed {len(internal_components)} components using external API")
            return internal_components
            
        except Exception as e:
            logger.error(f"External API parsing failed: {e}")
            raise
    
    def _convert_external_component(self, external_component: Component) -> Component:
        """Convert external API component to internal format"""
        # This method handles the conversion between external API format
        # and our internal component format
        
        # For now, we'll use the component as-is
        # In a real implementation, you might need to:
        # - Convert coordinate systems
        # - Normalize metadata formats
        # - Map external properties to internal properties
        
        return external_component
    
    async def _parse_dxf_file(self, file_path: Path) -> List[Component]:
        """Parse file DXF/DWG"""
        components = []
        
        try:
            # Load DXF file
            doc = ezdxf.readfile(str(file_path))
            modelspace = doc.modelspace()
            
            # Group entities by layers or blocks
            entities_by_layer = {}
            for entity in modelspace:
                layer_name = entity.dxf.layer
                if layer_name not in entities_by_layer:
                    entities_by_layer[layer_name] = []
                entities_by_layer[layer_name].append(entity)
            
            # Create components from layers
            for layer_name, entities in entities_by_layer.items():
                component = await self._create_component_from_entities(
                    layer_name, entities, file_path
                )
                if component:
                    components.append(component)
            
            # If no layers, create components from individual entities
            if not components:
                components = await self._create_components_from_entities(
                    list(modelspace), file_path
                )
                
        except Exception as e:
            logger.error(f"Error parsing DXF file {file_path}: {e}")
            raise
        
        return components
    
    async def _parse_3d_file(self, file_path: Path) -> List[Component]:
        """Parse file 3D (STL, OBJ, PLY)"""
        components = []
        
        try:
            # Load 3D mesh
            mesh = trimesh.load(str(file_path))
            
            # If it's a scene with multiple meshes
            if hasattr(mesh, 'geometry'):
                for name, geometry in mesh.geometry.items():
                    component = await self._create_component_from_mesh(
                        name, geometry, file_path
                    )
                    if component:
                        components.append(component)
            else:
                # Single mesh
                component = await self._create_component_from_mesh(
                    "main_component", mesh, file_path
                )
                if component:
                    components.append(component)
                    
        except Exception as e:
            logger.error(f"Error parsing 3D file {file_path}: {e}")
            raise
        
        return components
    
    async def _create_component_from_entities(
        self, 
        layer_name: str, 
        entities: List, 
        file_path: Path
    ) -> Optional[Component]:
        """Tạo component từ entities DXF"""
        if not entities:
            return None
        
        # Extract metadata from entities
        metadata = {
            "layer": layer_name,
            "entity_count": len(entities),
            "entity_types": list(set(type(e).__name__ for e in entities))
        }
        
        # Check for navigator/name properties
        has_navigator = False
        original_name = None
        
        # Look for text entities that might be names
        for entity in entities:
            if hasattr(entity, 'dxf') and hasattr(entity.dxf, 'text'):
                if entity.dxf.text and len(entity.dxf.text.strip()) > 0:
                    original_name = entity.dxf.text.strip()
                    has_navigator = True
                    break
        
        # Analyze shape and dimensions
        shape_type, dimensions = self._analyze_entities_shape(entities)
        size_category = self._categorize_size(dimensions)
        position = self._analyze_position(entities)
        
        component = Component(
            id=f"{file_path.stem}_{layer_name}",
            name=original_name,
            original_name=original_name,
            has_navigator=has_navigator,
            shape_type=shape_type,
            size_category=size_category,
            position=position,
            dimensions=dimensions,
            metadata=metadata
        )
        
        return component
    
    async def _create_component_from_mesh(
        self, 
        name: str, 
        mesh: trimesh.Trimesh, 
        file_path: Path
    ) -> Optional[Component]:
        """Tạo component từ 3D mesh"""
        if not hasattr(mesh, 'vertices') or len(mesh.vertices) == 0:
            return None
        
        # Extract metadata
        metadata = {
            "vertex_count": len(mesh.vertices),
            "face_count": len(mesh.faces) if hasattr(mesh, 'faces') else 0,
            "volume": float(mesh.volume) if hasattr(mesh, 'volume') else 0,
            "surface_area": float(mesh.surface_area) if hasattr(mesh, 'surface_area') else 0
        }
        
        # Analyze shape
        shape_type = self._analyze_mesh_shape(mesh)
        dimensions = self._extract_mesh_dimensions(mesh)
        size_category = self._categorize_size(dimensions)
        position = self._analyze_mesh_position(mesh)
        
        # Check for name in metadata
        has_navigator = False
        original_name = None
        if hasattr(mesh, 'metadata') and mesh.metadata:
            if 'name' in mesh.metadata:
                original_name = mesh.metadata['name']
                has_navigator = True
        
        component = Component(
            id=f"{file_path.stem}_{name}",
            name=original_name,
            original_name=original_name,
            has_navigator=has_navigator,
            shape_type=shape_type,
            size_category=size_category,
            position=position,
            dimensions=dimensions,
            metadata=metadata
        )
        
        return component
    
    async def _create_components_from_entities(
        self, 
        entities: List, 
        file_path: Path
    ) -> List[Component]:
        """Tạo components từ individual entities"""
        components = []
        
        # Group entities by type and proximity
        entity_groups = self._group_entities_by_proximity(entities)
        
        for i, group in enumerate(entity_groups):
            component = await self._create_component_from_entities(
                f"component_{i}", group, file_path
            )
            if component:
                components.append(component)
        
        return components
    
    def _analyze_entities_shape(self, entities: List) -> tuple[ShapeType, Dict[str, float]]:
        """Phân tích hình dạng từ entities"""
        # Simplified shape analysis
        entity_types = [type(e).__name__ for e in entities]
        
        if 'Circle' in entity_types:
            return ShapeType.CIRCLE, {"radius": 1.0}
        elif 'Line' in entity_types and len(entities) == 4:
            return ShapeType.SQUARE, {"width": 1.0, "height": 1.0}
        elif 'Arc' in entity_types:
            return ShapeType.CIRCLE, {"radius": 1.0}
        else:
            return ShapeType.COMPLEX, {"width": 1.0, "height": 1.0, "depth": 1.0}
    
    def _analyze_mesh_shape(self, mesh: trimesh.Trimesh) -> ShapeType:
        """Phân tích hình dạng từ mesh"""
        # Simplified shape analysis based on mesh properties
        if hasattr(mesh, 'is_watertight') and mesh.is_watertight:
            # Check if it's roughly spherical
            if hasattr(mesh, 'convex_hull'):
                hull = mesh.convex_hull
                if hasattr(hull, 'volume') and hasattr(mesh, 'volume'):
                    sphericity = mesh.volume / hull.volume
                    if sphericity > 0.8:
                        return ShapeType.SPHERE
            
            # Check if it's roughly cylindrical
            bounds = mesh.bounds
            width = bounds[1][0] - bounds[0][0]
            height = bounds[1][1] - bounds[0][1]
            depth = bounds[1][2] - bounds[0][2]
            
            if abs(width - height) < 0.1 and depth > width * 2:
                return ShapeType.CYLINDER
            elif width > height * 2 and height > depth * 2:
                return ShapeType.RECTANGLE
            elif abs(width - height) < 0.1 and abs(height - depth) < 0.1:
                return ShapeType.SQUARE
        
        return ShapeType.COMPLEX
    
    def _extract_mesh_dimensions(self, mesh: trimesh.Trimesh) -> Dict[str, float]:
        """Trích xuất kích thước từ mesh"""
        bounds = mesh.bounds
        return {
            "width": float(bounds[1][0] - bounds[0][0]),
            "height": float(bounds[1][1] - bounds[0][1]),
            "depth": float(bounds[1][2] - bounds[0][2])
        }
    
    def _categorize_size(self, dimensions: Dict[str, float]) -> SizeCategory:
        """Phân loại kích thước"""
        if not dimensions:
            return SizeCategory.MEDIUM
        
        # Use the largest dimension for categorization
        max_dimension = max(dimensions.values()) if dimensions.values() else 1.0
        
        if max_dimension < 10:
            return SizeCategory.SMALL
        elif max_dimension < 100:
            return SizeCategory.MEDIUM
        else:
            return SizeCategory.LARGE
    
    def _analyze_position(self, entities: List) -> PositionType:
        """Phân tích vị trí từ entities"""
        # Simplified position analysis
        # In a real implementation, this would analyze the actual positions
        return PositionType.CENTER
    
    def _analyze_mesh_position(self, mesh: trimesh.Trimesh) -> PositionType:
        """Phân tích vị trí từ mesh"""
        # Simplified position analysis
        return PositionType.CENTER
    
    def _group_entities_by_proximity(self, entities: List) -> List[List]:
        """Nhóm entities theo khoảng cách gần nhau"""
        # Simplified grouping - in reality would use spatial clustering
        groups = []
        for entity in entities:
            groups.append([entity])
        return groups
