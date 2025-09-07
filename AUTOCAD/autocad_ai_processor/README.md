# AutoCAD 3D to 2D AI Processor

Hệ thống chuyển đổi file AutoCAD 3D thành các file 2D với tích hợp AI để nhận dạng và đặt tên các thành phần.

## Tính năng chính

- **Upload file AutoCAD 3D**: Hỗ trợ các format DWG, DXF, STL, OBJ, PLY
- **External API Integration**: Tích hợp với các API CAD viewer tốt nhất thế giới
- **AI Component Analysis**: Nhận dạng và phân tích các thành phần 3D
- **Smart Naming**: Tự động đặt tên cho các thành phần không có tên
- **Multi-view Generation**: Tạo các view 2D (top, front, side, isometric)
- **Batch Processing**: Xử lý nhiều thành phần cùng lúc
- **Fallback System**: Tự động chuyển đổi API provider khi cần
- **RESTful API**: API đầy đủ với FastAPI

## Cài đặt

### 1. Clone repository
```bash
git clone <repository-url>
cd autocad_ai_processor
```

### 2. Tạo virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate  # Windows
```

### 3. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 4. Cấu hình API Keys
```bash
# Copy file cấu hình
cp config/api_keys.env.example .env

# Chỉnh sửa file .env với API keys thật
# Quan trọng: Cần có ít nhất 1 API key để hệ thống hoạt động
```

### 5. Chạy ứng dụng
```bash
python main.py
```

Ứng dụng sẽ chạy tại: `http://localhost:8000`

## API Documentation

### Endpoints chính

#### 1. Upload CAD File
```http
POST /api/cad/upload
Content-Type: multipart/form-data
Body: file (AutoCAD 3D file)
```

#### 2. Process CAD File
```http
POST /api/cad/process
Body: { "file_id": "string" }
```

#### 3. Get Processing Status
```http
GET /api/cad/process/{process_id}/status
```

#### 4. Download Results
```http
GET /api/cad/process/{process_id}/download
```

#### 5. Download Specific File
```http
GET /api/cad/process/{process_id}/download/{filename}
```

#### 6. Get API Providers Status
```http
GET /api/cad/providers
```

#### 7. Test API Provider
```http
POST /api/cad/providers/{provider}/test
```

### Interactive API Documentation

Truy cập Swagger UI tại: `http://localhost:8000/docs`
Truy cập ReDoc tại: `http://localhost:8000/redoc`

## Cấu trúc Project

```
autocad_ai_processor/
├── main.py                 # FastAPI application
├── requirements.txt        # Dependencies
├── README.md              # Documentation
├── models/
│   ├── __init__.py
│   └── schemas.py         # Pydantic models
├── services/
│   ├── __init__.py
│   ├── file_service.py    # File management
│   ├── cad_parser.py      # CAD file parsing
│   ├── component_analyzer.py  # Component analysis
│   ├── ai_service.py      # AI analysis
│   ├── name_generator.py  # Name generation
│   └── output_service.py  # 2D file generation
├── utils/                 # Utility functions
├── config/               # Configuration files
├── uploads/              # Upload directory
└── outputs/              # Output directory
```

## Workflow

1. **Upload**: User upload file AutoCAD 3D
2. **External API Parse**: Gửi file đến external API để parse (Autodesk Forge, ShareCAD, etc.)
3. **Component Extraction**: Trích xuất components từ structured data
4. **AI Analysis**: AI phân tích từng component
5. **Smart Naming**: Tạo tên cho components không có tên
6. **2D Generation**: Tạo các file 2D bằng external API hoặc local processing
7. **Post-processing**: Thêm component names vào file 2D
8. **Download**: User download kết quả

## External API Providers

### 🏆 Khuyến nghị chính: **Autodesk Forge**
- **Ưu điểm**: Chính thức từ Autodesk, tương thích 100% với AutoCAD
- **Chi phí**: 100 conversions miễn phí/tháng, sau đó $0.05/conversion
- **Tính năng**: Đầy đủ cho mọi use case

### 🔄 Fallback options:
- **ShareCAD**: Miễn phí, giới hạn 50MB/file
- **CADViewer360**: $99/tháng, professional features
- **CloudConvert**: $8/tháng, general purpose

### 📊 So sánh chi tiết:
Xem file `api_comparison_analysis.md` để biết thêm chi tiết về từng provider.

## AI Naming Rules

### Format tên: `[Function]_[Shape]_[Size]_[Position]_[Index]`

Ví dụ:
- `Bearing_Circle_Large_Top_001`
- `Shaft_Cylinder_Medium_Center_002`
- `Housing_Square_Small_Bottom_003`

### Component Types
- Bearing, Shaft, Housing, Gear, Bolt, Nut, Washer, Spring

### Shape Types
- Circle, Square, Triangle, Rectangle, Cylinder, Sphere, Complex

### Size Categories
- Small, Medium, Large

### Position Types
- Top, Bottom, Left, Right, Center, Front, Back

## Configuration

### Environment Variables
```bash
# File upload settings
MAX_FILE_SIZE=100MB
UPLOAD_DIR=uploads
OUTPUT_DIR=outputs

# AI settings
AI_CONFIDENCE_THRESHOLD=0.7
BATCH_SIZE=5

# Server settings
HOST=0.0.0.0
PORT=8000
```

## Error Handling

Hệ thống có xử lý lỗi toàn diện cho:
- File upload errors
- Parsing errors
- AI analysis failures
- Output generation errors

## Performance

- **Async Processing**: Sử dụng background tasks
- **Batch Processing**: Xử lý nhiều components cùng lúc
- **Caching**: Cache kết quả AI
- **Progress Tracking**: Real-time progress updates

## Security

- **File Validation**: Kiểm tra file type và size
- **Sandbox Processing**: Chạy AI trong sandbox
- **Data Privacy**: Không lưu trữ dữ liệu nhạy cảm
- **Access Control**: Authentication và authorization

## Testing

### Unit Tests
```bash
python -m pytest tests/
```

### API Tests
```bash
python -m pytest tests/api/
```

## Deployment

### Docker
```bash
docker build -t autocad-ai-processor .
docker run -p 8000:8000 autocad-ai-processor
```

### Production
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Contributing

1. Fork repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## License

MIT License

## Support

Liên hệ: [email@example.com]

## Changelog

### v1.0.0
- Initial release
- Basic CAD parsing
- AI component analysis
- 2D file generation
- RESTful API
