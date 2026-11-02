from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from functools import wraps

app = Flask(__name__)
CORS(app)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

SECRET_TOKEN = "YOUR_API_TOKEN"



SECRET_TOKEN = "YOUR_API_TOKEN"

latest_audit_data = {
    "hostname": "Redacted",
    "os": "Redacted",
    "ip_address": "Redacted",
    "cpu_usage": "0",
    "ram_usage": "0",
    "disk_free_gb": "0"
}

def require_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing Token"}), 401
        
        token = auth_header.split(" ")[1]
        if token != SECRET_TOKEN:
            return jsonify({"error": "Invalid Token. Access denied"}), 403
            
        return f(*args, **kwargs)
    return decorated

@app.route('/api/audit', methods=['POST'])
@require_token
def receive_audit():
    global latest_audit_data
    latest_audit_data = request.json
    print("[+] New Data:", latest_audit_data)
    return jsonify({"status": "success", "message": "Data recieved"}), 200

@app.route('/api/audit/latest', methods=['GET'])
@require_token
def get_latest_audit():
    return jsonify(latest_audit_data), 200


if __name__ == '__main__':
    app.run()