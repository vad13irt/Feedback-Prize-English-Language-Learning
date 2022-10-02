from transform import Transform
from typing import Optional, Dict
import contractions
import numpy as np
import re


class SlangConverter(Transform):
    def __init__(
        self, 
        level: str = "text",
        slang_dict: Optional[Dict[str, str]] = None, 
        convert_full_to_slang: bool = False,
        punctuations: str = ".,:?! ", 
        p: float = 0.5,
    ):
        super().__init__(p)
        
        self.slang_dict = slang_dict
        self.level = level
        self.punctuations = punctuations
        self.convert_full_to_slang = convert_full_to_slang
        
        if self.level not in ("word", "text"):
            raise ValueError(f"`level` must be one of ['word', 'text'], but given {self.level}")
        
        if self.slang_dict is None:
            self.slang_dict = contractions.contractions_dict
            self.slang_dict.update(contractions.slang_dict)
            
        self.reversed_slang_dict = {full:slang for slang, full in self.slang_dict.items()}
    
    def replace_function(self, match: re.Match, data: Dict[str, str]) -> str:
        text = match.group(0)
        punctuation_after = text[-1]
        punctuation_before = text[0]
        text = text[1:-1]
        
        try:
            slang = text.strip()
            full = data[slang]
        except KeyError:
            return text
        
        return punctuation_before + full + punctuation_after
            
    def apply(self, text: str) -> str:
        if np.random.uniform() < self.p or self.level == "word":
            text = self.transform(text)
        
        return text
        
    def transform(self, text: str) -> str:
        for slang, full in self.slang_dict.items():
            transformed = False
            does_apply = (np.random.uniform() < self.p or self.level == "text")
            if slang in text and does_apply:
                func = lambda match: self.replace_function(match, data=self.slang_dict)
                text = re.sub(f"[{self.punctuations}]{slang}[{self.punctuations}]", func, text)
                transformed = True
                
            if full in text and not transformed and does_apply and self.convert_full_to_slang:
                func = lambda match: self.replace_function(match, data=self.reversed_slang_dict)
                text = re.sub(f"[{self.punctuations}]{full}[{self.punctuations}]", func, text)
    
        return text