from transform import Transform
from typing import Optional, Dict
import requests
import json
import random


class AccentConverter(Transform):
    def __init__(self, accent_dict: Optional[Dict[str, str]] = None, p: float = 0.5):
        super().__init__(p)
        
        self.accent_dict = accent_dict
        
        if self.accent_dict is None:
            request_url = "https://raw.githubusercontent.com/hyperreality/American-British-English-Translator/master/data/british_spellings.json"
            response = requests.get(request_url)
            self.accent_dict = json.loads(response.text)
            
        self.reversed_accent_dict = {v:k for k, v in self.accent_dict.items()}
            
    def transform(self, text: str) -> str:
        dict_index = random.randint(a=0, b=1)
        accent_dict = self.accent_dict if bool(dict_index) else self.reversed_accent_dict
        
        for k, v in accent_dict.items():
            text = text.replace(k, v)
            
        return text