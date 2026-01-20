import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import RSLPStemmer

from app.utils.exceptions import NLPProcessingException


_nltk_downloaded = False


def _ensure_nltk_data():
    global _nltk_downloaded
    if _nltk_downloaded:
        return
    
    try:
        nltk.download('punkt', quiet=True)
        nltk.download('punkt_tab', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('rslp', quiet=True)
        _nltk_downloaded = True
    except Exception as e:
        raise NLPProcessingException(f"Erro ao baixar dados do NLTK: {str(e)}")


def extract_keywords(text: str) -> str:
    if not text or not text.strip():
        raise NLPProcessingException("Texto não pode estar vazio para extração de keywords")
    
    _ensure_nltk_data()
    
    try:
        normalized_text = text.lower()
        
        cleaned_text = re.sub(r'[^a-záéíóúâêîôûãõç\s]', ' ', normalized_text)
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
        
        try:
            tokens = word_tokenize(cleaned_text, language='portuguese')
        except LookupError:
            tokens = word_tokenize(cleaned_text)
        
        stop_words = set(stopwords.words('portuguese'))
        filtered_tokens = [token for token in tokens if token not in stop_words and len(token) >= 3]
        
        stemmer = RSLPStemmer()
        stemmed_tokens = [stemmer.stem(token) for token in filtered_tokens]
        
        unique_stems = list(dict.fromkeys(stemmed_tokens))
        
        keywords = ' '.join(unique_stems)
        
        return keywords.strip()
    except Exception as e:
        raise NLPProcessingException(f"Erro ao processar texto com NLP: {str(e)}")
