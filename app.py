# app.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from config import Config

# Khởi tạo Flask App
app = Flask(__name__)
app.config.from_object(Config)

# Khởi tạo SQLAlchemy
db = SQLAlchemy(app)

# Model cho Product
class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=lambda: datetime.now(timezone.UTC))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': float(self.price),
            'quantity': self.quantity,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

# API Routes

# 1. Lấy danh sách sản phẩm
@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        # Lấy tham số phân trang từ query string
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Query với phân trang
        products = Product.query.paginate(page=page, per_page=per_page)
        
        return jsonify({
            'success': True,
            'data': {
                'products': [product.to_dict() for product in products.items],
                'total': products.total,
                'page': products.page,
                'pages': products.pages,
                'per_page': per_page
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# 2. Lấy chi tiết một sản phẩm
@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'success': False, 'message': 'Không tìm thấy sản phẩm'}), 404
            
        return jsonify({
            'success': True,
            'data': product.to_dict()
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# 3. Thêm sản phẩm mới
@app.route('/api/products', methods=['POST'])
def create_product():
    try:
        data = request.get_json()
        
        # Kiểm tra dữ liệu đầu vào
        if not all(key in data for key in ['name', 'price', 'quantity']):
            return jsonify({
                'success': False, 
                'message': 'Thiếu thông tin bắt buộc'
            }), 400
            
        # Tạo sản phẩm mới
        new_product = Product(
            name=data['name'],
            description=data.get('description'),
            price=data['price'],
            quantity=data['quantity']
        )
        
        # Lưu vào database
        db.session.add(new_product)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Tạo sản phẩm thành công',
            'data': new_product.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

# 4. Cập nhật sản phẩm
@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'success': False, 'message': 'Không tìm thấy sản phẩm'}), 404
            
        data = request.get_json()
        
        # Cập nhật thông tin
        if 'name' in data:
            product.name = data['name']
        if 'description' in data:
            product.description = data['description']
        if 'price' in data:
            product.price = data['price']
        if 'quantity' in data:
            product.quantity = data['quantity']
            
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Cập nhật sản phẩm thành công',
            'data': product.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

# 5. Xóa sản phẩm
@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'success': False, 'message': 'Không tìm thấy sản phẩm'}), 404
            
        db.session.delete(product)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Xóa sản phẩm thành công'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

# Tạo bảng khi chạy lần đầu
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)