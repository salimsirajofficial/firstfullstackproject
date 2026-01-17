import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.environ.get('DATABASE_URL') or f"sqlite:///{os.path.join(BASE_DIR, 'registrations.db')}"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_PATH
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app, resources={r"/api/*": {"origins": "*"}})

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.Text, nullable=True)

@app.route('/api/health')
def health():
    return jsonify({'status': 'ok'})

@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json() or {}
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    comment = data.get('comment')

    if not username or not email or not password:
        return jsonify({'error': 'username, email and password required'}), 400

    user = User(username=username, email=email, password=password, comment=comment)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': f'User {username} saved', 'id': user.id}), 201

@app.route('/api/registrants', methods=['GET'])
def api_registrants():
    users = User.query.order_by(User.id.desc()).all()
    return jsonify([{'id':u.id,'username':u.username,'email':u.email,'comment':u.comment} for u in users])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)