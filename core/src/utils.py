import re
from core.config import Config

def postprocess_classification_respond(response):
    match = re.search(r'\d+', response)
    if match:
        res = int(match.group(0))
        if res < len(Config.CLASSIFICATIONS) and res > 0:
            return res
    return 0