import io
from fastapi import UploadFile

from app.utils.exceptions import InvalidFileException
from app.utils.validators import validate_file


async def read_file(file: UploadFile) -> str:
    validate_file(file)
    
    content = await file.read()
    
    if len(content) == 0:
        raise InvalidFileException("Arquivo está vazio")
    
    if len(content) > 10 * 1024 * 1024:
        raise InvalidFileException("Arquivo excede o tamanho máximo de 10MB")
    
    file_extension = file.filename.lower().split('.')[-1] if file.filename else ''
    
    try:
        if file_extension == 'pdf':
            return _read_pdf(content)
        elif file_extension == 'txt':
            return _read_text(content)
        else:
            raise InvalidFileException("Formato de arquivo não suportado")
    except Exception as e:
        if isinstance(e, InvalidFileException):
            raise
        raise InvalidFileException(f"Erro ao ler arquivo: {str(e)}")


def _read_pdf(content: bytes) -> str:
    try:
        from pypdf import PdfReader
        
        pdf_file = io.BytesIO(content)
        reader = PdfReader(pdf_file)
        
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        
        if not text.strip():
            raise InvalidFileException("Arquivo PDF não contém texto legível")
        
        return text.strip()
    except ImportError:
        raise InvalidFileException("Biblioteca pypdf não está instalada")
    except Exception as e:
        raise InvalidFileException(f"Erro ao processar PDF: {str(e)}")


def _read_text(content: bytes) -> str:
    try:
        text = content.decode('utf-8')
    except UnicodeDecodeError:
        try:
            text = content.decode('latin1')
        except UnicodeDecodeError:
            raise InvalidFileException("Não foi possível decodificar o arquivo de texto")
    
    if not text.strip():
        raise InvalidFileException("Arquivo de texto está vazio")
    
    return text.strip()
