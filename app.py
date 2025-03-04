from flask import Flask, request
import uuid
import hashlib , platform ,os 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# إعداد قاعدة البيانات
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # يمكنك تغييرها إلى MySQL أو PostgreSQL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# تعريف جدول المستخدمين
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    device_uuid = db.Column(db.String(64), nullable=False)  # زيادة الحجم ليحتوي على SHA-256

# دالة للحصول على UUID للجهاز باستخدام MAC address
def get_device_uuid():
    # الحصول على MAC address
    mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0, 8 * 6, 8)])
    device_info = f"{platform.node()}-{platform.system()}-{platform.release()}-{platform.processor()}"
    ip_address = request.environ.get('REMOTE_ADDR')
    
    # توليد UUID باستخدام MAC address عبر تشفير SHA-256
    return hashlib.sha256((mac_address + ip_address + device_info).encode()).hexdigest()

@app.route('/')
def index():
    device_uuid = get_device_uuid()  # الحصول على UUID للجهاز
    return f"Device UUID: {device_uuid}"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        password = request.form.get('password')

        if user_name and password:
            device_uuid = get_device_uuid()  # استخراج UUID للجهاز
            
            # التحقق من أن المستخدم غير مسجل مسبقًا
            existing_user = User.query.filter_by(user_name=user_name).first()
            if existing_user:
                return "Username already exists!"

            user = User(user_name=user_name, password=password, device_uuid=device_uuid)
            db.session.add(user)
            db.session.commit()
            return 'User registered successfully!'

    return """
    <html>
        <body>
            <h1>Register</h1>
            <form action="/register" method="post">
                <label for="user_name">User name:</label>
                <input type="text" id="user_name" name="user_name" required>
                <br>
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required>
                <br>
                <input type="submit" value="Register">
            </form>
        </body>
    </html>
    """    

@app.route('/login', methods=['GET', 'POST'])  # ✅ إضافة methods=['GET', 'POST']
def login():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        password = request.form.get('password')

        if user_name and password:
            user = User.query.filter_by(user_name=user_name).first()
            if user and user.password == password:
                device_uuid = get_device_uuid()  # استخراج UUID للجهاز
                
                # التحقق إذا كان UUID الجهاز الذي سجل الدخول يتطابق مع UUID الجهاز المسجل
                if device_uuid == user.device_uuid:
                    return 'Login successful!'
                else:
                    return "Please use the device you registered with"

    return """
    <html>
        <body>
            <h1>Login</h1>
            <form action="/login" method="post">
                <label for="user_name">User name:</label>
                <input type="text" id="user_name" name="user_name" required>
                <br>
                <label for="password">Password:</label>  
                <input type="password" id="password" name="password" required>
                <br>
                <input type="submit" value="Login">
            </form>
        </body>
    </html>
    """ 

if __name__ == '__main__':
    app.run(debug=True, host="192.168.1.5", port=8000)
