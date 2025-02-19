from flask import Flask, request, jsonify, render_template, Response
import requests
import json

app = Flask(__name__)

OLLAMA_API_ENDPOINT = "http://localhost:11434/api/generate"  # Local Ollama API endpoint

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/call_api', methods=['POST'])
def call_api():
    text_input = request.form.get('text')
    payload = {
        "model": "llama3.2", "prompt": text_input
    }
    
    def generate():
        with requests.post(OLLAMA_API_ENDPOINT, json=payload, stream=True) as response:
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        yield line.decode('utf-8') + "\n"  # Send raw JSON back to frontend
            else:
                yield f'{{"error": "Received status code {response.status_code}"}}\n'
    
    return Response(generate(), content_type='text/plain')

if __name__ == '__main__':
    app.run(debug=True)