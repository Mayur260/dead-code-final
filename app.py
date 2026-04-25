from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from analyzers.python_analyzer import analyze_python
from analyzers.js_analyzer import analyze_js
from analyzers.cpp_analyzer import analyze_cpp
from ai_helper import explain_dead_code

app = Flask(__name__, static_folder=".")
CORS(app)

@app.route('/')
def serve_frontend():
    return send_from_directory('.', 'index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()

    if not data or "code" not in data:
        return jsonify({"error": "No code provided"}), 400

    code = data["code"]
    language = data.get("language", "python").lower()

    try:
        if language == "python":
            dead_code = analyze_python(code)
            error_msg = "Invalid Python code"
        elif language == "js" or language == "javascript":
            dead_code = analyze_js(code)
            error_msg = "Invalid JavaScript code"
        elif language == "cpp" or language == "c++":
            dead_code = analyze_cpp(code)
            error_msg = "Invalid C/C++ code"
        else:
            return jsonify({"error": f"Language '{language}' not supported"}), 400

        # Check for syntax/analyzer errors
        if dead_code == [error_msg]:
            return jsonify({"error": error_msg}), 400

        try:
            ai_response = explain_dead_code(code, dead_code)
        except Exception as e:
            print("AI ERROR:", e)
            ai_response = "AI suggestions unavailable"

        return jsonify({
            "status": "success",
            "dead_code": dead_code,
            "summary": f"{len(dead_code)} unused symbols found" if dead_code else "No dead code found",
            "ai_suggestions": ai_response
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == '__main__':
    app.run(debug=True)