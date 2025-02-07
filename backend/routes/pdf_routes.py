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
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['file']
        if not allowed_file(file.filename):
            return jsonify({'error': 'Tipo de arquivo não permitido'}), 400

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
            return jsonify({
                'error': f'Erro na conversão: {str(e)}',
                'details': 'Verifique o formato do arquivo'
            }), 500

    except Exception as e:
        return jsonify({
            'error': f'Erro na conversão: {str(e)}',
            'details': 'Verifique o formato do arquivo'
        }), 500

@pdf_blueprint.route('/comprimir', methods=['POST'])
def comprimir_pdf():
    try:
        # Obter dados da requisição
        if request.is_json:
            data = request.get_json()
            if 'pdfBase64' not in data:
                return jsonify({
                    "erro": "Dados inválidos",
                    "detalhes": "Campo 'pdfBase64' é obrigatório"
                }), 400
            pdf_data = base64.b64decode(data['pdfBase64'])
        else:
            if 'pdf' not in request.files:
                return jsonify({
                    "erro": "Dados inválidos",
                    "detalhes": "Arquivo PDF é obrigatório"
                }), 400
            pdf_data = request.files['pdf'].read()

        # Simular compressão (implementar lógica real aqui)
        compressed_data = pdf_data  # Substituir por compressão real
        
        return jsonify({
            "mensagem": "PDF comprimido com sucesso",
            "pdfComprimidoBase64": base64.b64encode(compressed_data).decode('utf-8')
        }), 200

    except Exception as e:
        return jsonify({
            "erro": "Falha ao comprimir PDF",
            "detalhes": str(e)
        }), 500