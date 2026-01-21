import os
from typing import List

CORS_ORIGINS: List[str] = os.getenv('CORS_ORIGINS', '*').split(',')
RATE_LIMIT_PER_MINUTE: int = int(os.getenv('RATE_LIMIT_PER_MINUTE', '10'))
