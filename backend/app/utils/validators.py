import os
from fastapi import UploadFile

from app.utils.exceptions import InvalidFileException, InvalidTextException

MAX_FILE_SIZE = 10 * 1024 * 1024
MAX_TEXT_LENGTH = 50000
ALLOWED_EXTENSIONS = {'.pdf', '.txt'}


def validate_file(file: UploadFile) -> None:
    if not file.filename:
        raise InvalidFileException("Nome do arquivo não fornecido")
    
    file_extension = os.path.splitext(file.filename.lower())[1]
    if file_extension not in ALLOWED_EXTENSIONS:
        raise InvalidFileException(f"Apenas arquivos {', '.join(ALLOWED_EXTENSIONS)} são aceitos")
    
    if hasattr(file, 'size') and file.size and file.size > MAX_FILE_SIZE:
        raise InvalidFileException(f"Arquivo excede o tamanho máximo de {MAX_FILE_SIZE / (1024*1024)}MB")


def validate_text(text: str) -> None:
    if not text or not text.strip():
        raise InvalidTextException("Texto não pode estar vazio")
    
    if len(text) > MAX_TEXT_LENGTH:
        raise InvalidTextException(f"Texto excede o limite de {MAX_TEXT_LENGTH} caracteres")
    
    try:
        text.encode('utf-8')
    except UnicodeEncodeError:
        raise InvalidTextException("Texto contém caracteres inválidos")
