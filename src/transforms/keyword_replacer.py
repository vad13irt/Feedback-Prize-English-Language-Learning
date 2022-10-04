from transform import Transform
from typing import Optional, Dict, List
import numpy as np
import random


class KeywordReplacer(Transform):
    def __init__(
        self, 
        keywords: Optional[Dict[str, List[str]]],
        level: str = "text", 
        p: float = 0.5, 
    ):
        super().__init__(p)
        
        self.keywords = keywords
        self.level = level
               
        if self.level not in ("word", "text"):
            raise ValueError(f"`level` must be one of ['word', 'text'], but given {self.level}")
        
        
    def apply(self, text: str) -> str:
        if np.random.uniform() < self.p or self.level == "word":
            text = self.transform(text)
        
        return text
            
    def transform(self, text: str) -> str:
        for key, words in self.keywords.items():
            if (key in text and len(words) > 0) and (self.level == "text" or np.random.uniform() < self.p):
                random_word = random.choice(words)
                text = text.replace(key, random_word)
        
        return text