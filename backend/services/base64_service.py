import base64
import io

def base64_to_file(base64_str):
    try:
        file_data = base64.b64decode(base64_str)
        return io.BytesIO(file_data)
    except Exception as e:
        print(f"Erro na conversão: {e}")
        return None

def file_to_base64(file_path):  
    try:
        with open(file_path, 'rb') as file:
            return base64.b64encode(file.read()).decode('utf-8')
    except Exception as e:
        print(f"Erro na conversão arquivo para Base64: {e}")
        return None

def base64_to_pdf(base64_str, output_path):
    try:
        pdf_data = base64.b64decode(base64_str)
        with open(output_path, 'wb') as pdf_file:
            pdf_file.write(pdf_data)
        return True
    except Exception as e:
        print(f"Erro na conversão Base64 para PDF: {e}")
        return False

def pdf_to_base64(pdf_path):
    try:
        with open(pdf_path, 'rb') as pdf_file:
            return base64.b64encode(pdf_file.read()).decode('utf-8')
    except Exception as e:
        print(f"Erro na conversão PDF para Base64: {e}")
        return None