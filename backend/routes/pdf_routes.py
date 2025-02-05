from flask import Blueprint, request, jsonify, send_file, current_app
from services.base64_service import file_to_base64, base64_to_file
from services.file_utils import allowed_file, save_uploaded_file
import os
import filetype
import base64
import io

pdf_blueprint = Blueprint('pdf', __name__)

@pdf_blueprint.route('/base64-to-file', methods=['POST'])
def handle_base64_to_file():
    try:
        data = request.json
        if not data or 'base64' not in data:
            return jsonify({'error': 'Dados incompletos'}), 400
        
        # Cria um BytesIO a partir do base64
        file_data = base64.b64decode(data["base64"])
        file_stream = io.BytesIO(file_data)
        
        # Mantém o objeto na memória durante todo o processo
        file_stream.seek(0)
        kind = filetype.guess(file_stream.read())
        mime = kind.mime if kind else 'application/octet-stream'
        file_stream.seek(0)

        return send_file(
            file_stream,
            as_attachment=True,
            download_name=f'converted.{data.get("extension", "bin")}',
            mimetype=mime,
            conditional=False  # Impede o fechamento automático
        )

    except Exception as e:
        current_app.logger.error(f'Erro: {str(e)}')
        return jsonify({'error': str(e)}), 500

@pdf_blueprint.route('/file-to-base64', methods=['POST'])
def handle_file_to_base64():
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400
        
    file = request.files['file']
    if file and allowed_file(file.filename):
        try:
            file_path = save_uploaded_file(file)
            base64_str = file_to_base64(file_path)
            if base64_str:
                return jsonify({
                    'base64': base64_str,
                    'mime_type': file.mimetype  # Envia o tipo MIME real
                })
            return jsonify({'error': 'Conversão falhou'}), 500
        except Exception as e:
            current_app.logger.error(f'Erro na conversão: {str(e)}')
            return jsonify({'error': str(e)}), 500
    return jsonify({'error': 'Tipo de arquivo não permitido'}), 400

@pdf_blueprint.route('/comprimir', methods=['POST'])
def comprimir_pdf():
    try:
        if request.is_json:
            data = request.get_json()
            if 'pdfBase64' not in data:
                return jsonify({"error": "Dados inválidos"}), 400
            file_stream = base64_to_file(data['pdfBase64'])
        else:
            if 'pdf' not in request.files:
                return jsonify({"error": "Nenhum arquivo recebido"}), 400
            file_stream = request.files['pdf'].stream

        # Lógica de compressão aqui (usando PyPDF2 ou outra lib)
        # ... (implementar compressão)
        
        return send_file(
            file_stream,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='documento-comprimido.pdf'
        )
        
    except Exception as e:
        current_app.logger.error(f'Erro na compressão: {str(e)}')
        return jsonify({"error": str(e)}), 500