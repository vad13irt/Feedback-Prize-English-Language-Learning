from transform import Transform
from utils import join_text_parts
from nltk.tokenize import word_tokenize
from word2number.w2n import word_to_num as words2num
from num2words import num2words
import numpy as np
import re


class NumberToWordsConverter(Transform):      
    def __init__(self, level: str = "text", p: float = 0.5):
        super().__init__(p)
        self.level = level
        
        if self.level not in ("text", "word"):
            raise ValueError(f"`level` must be one of ['text', 'word'], but given {self.level}")
            
    
    def apply(self, text: str) -> str:
        if np.random.uniform() < self.p or self.level == "word":
            text = self.transform(text)
        
        return text
    
    def transform(self, text: str) -> str:
        numbers = re.findall('[0-9]+', text)
        
        if len(numbers) > 0:
            words = word_tokenize(text)
            new_words = []
            for word in words:
                does_apply = (np.random.uniform() < self.p or self.level == "text")
                if word.isdigit() and does_apply:
                    word = num2words(int(word))
                elif does_apply:
                    try:
                        word = words2num(word)
                    except ValueError:
                        pass

                new_words.append(word)
            
            text = join_text_parts(new_words)
            
        return text    