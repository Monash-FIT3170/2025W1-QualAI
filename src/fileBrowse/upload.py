from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files.get('file')
    if not uploaded_file:
        return jsonify({"error": "No file uploaded"}), 400

    try:
        # Make sure the uploads directory exists
        os.makedirs('uploads', exist_ok=True)

        filepath = os.path.join('uploads', uploaded_file.filename)
        uploaded_file.save(filepath)

        result = process_file(filepath)
        return jsonify({"status": "success", "result": result})
    except Exception as e:
        print("Error during file upload:", e)
        return jsonify({"error": str(e)}), 500

def process_file(path: str) -> str:
    # Read/process the file however you want
    with open(path, 'r') as f:
        content = f.read()
    print("HIIIIIIIIIIIIIIIIIIII")
    return f"File length: {len(content)}"

app.run()