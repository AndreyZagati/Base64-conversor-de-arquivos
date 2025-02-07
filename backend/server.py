from flask import Flask, render_template, current_app, jsonify
from routes.pdf_routes import pdf_blueprint
import os
import requests
import json

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static/uploads')
app.config['MAX_CONTENT_LENGTH'] = 60 * 1024 * 1024  # 60MB

# Garante que a pasta de uploads existe ao iniciar o app
with app.app_context():
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

app.register_blueprint(pdf_blueprint, url_prefix='/ms')

# Adicione esta nova rota
@app.route('/')
def index():
    return render_template('index.html')

url = "http://192.168.24.142:27016/ms/comprimir"  # Corrigido para /api/comprimir

payload = json.dumps({
  "pdfBase64": "string"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

# Adicione este handler de erros global
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({
        'error': 'Endpoint não encontrado',
        'caminho_correto': '/ms/file-to-base64'
    }), 404

@app.errorhandler(Exception)
def handle_exception(error):
    return jsonify({
        'error': 'Erro interno no servidor',
        'detalhes': str(error)
    }), 500

if __name__ == '__main__':
    app.run(debug=True)