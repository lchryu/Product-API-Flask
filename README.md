# Product Management API

Một RESTful API đơn giản để quản lý sản phẩm được xây dựng bằng Flask và MySQL.

## Tính năng

- ✨ CRUD Operations cho sản phẩm
- 📝 Hỗ trợ phân trang
- 🔍 Tìm kiếm sản phẩm theo ID
- 💾 Lưu trữ dữ liệu với MySQL
- 🌐 RESTful API endpoints

## Yêu cầu

- Python 3.8+
- MySQL 5.7+
- pip (Python package installer)

## Cài đặt

1. Clone repository
\```bash
git clone https://github.com/your-username/product-management-api.git
cd product-management-api
\```

2. Cài đặt các thư viện cần thiết
\```bash
pip install flask
pip install flask-sqlalchemy
pip install pymysql
\```

3. Tạo database MySQL
\```sql
CREATE DATABASE product_management;
USE product_management;

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    quantity INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
\```

4. Cấu hình database
Mở file `config.py` và cập nhật thông tin kết nối database:
\```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/product_management'
\```

5. Chạy ứng dụng
\```bash
python app.py
\```

## API Endpoints

### Lấy danh sách sản phẩm
\```http
GET /api/products?page=1&per_page=10
\```
#### Response
\```json
{
    "success": true,
    "data": {
        "products": [...],
        "total": 20,
        "page": 1,
        "pages": 2,
        "per_page": 10
    }
}
\```

### Lấy chi tiết sản phẩm
\```http
GET /api/products/{id}
\```
#### Response
\```json
{
    "success": true,
    "data": {
        "id": 1,
        "name": "Laptop Dell XPS 13",
        "description": "Laptop cao cấp của Dell",
        "price": 25000000,
        "quantity": 10,
        "created_at": "2024-03-06 15:30:00"
    }
}
\```

### Tạo sản phẩm mới
\```http
POST /api/products
Content-Type: application/json

{
    "name": "Laptop Dell XPS 13",
    "description": "Laptop cao cấp của Dell",
    "price": 25000000,
    "quantity": 10
}
\```

### Cập nhật sản phẩm
\```http
PUT /api/products/{id}
Content-Type: application/json

{
    "price": 26000000,
    "quantity": 8
}
\```

### Xóa sản phẩm
\```http
DELETE /api/products/{id}
\```

## Cấu trúc Project

\```
product_api/
├── config.py         # Cấu hình database
└── app.py           # File chính
\```

## Đóng góp

Mọi đóng góp đều được chào đón. Hãy tạo Pull Request để đóng góp.
