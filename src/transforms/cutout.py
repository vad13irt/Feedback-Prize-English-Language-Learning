from transform import Transform
from utils import join_text_parts
from nltk.tokenize import word_tokenize, sent_tokenize
import numpy as np
import math


class CutOut(Transform):
    def __init__(self, level: str = "word", fraction: float = 0.01, p: float = 0.5):
        super().__init__(p)
        
        self.level = level
        self.fraction = fraction
        self.p = p
        
        if self.level not in ("word", "sentence"):
            raise ValueError(f"`level` must be one of ['word', 'sentence'], but given {self.level}")
            
        if self.level == "word":
            self.__split_func = word_tokenize
        elif self.level == "sentence":
            self.__split_func = sent_tokenize
        
    def transform(self, text: str) -> str:
        segments = np.array(self.__split_func(text))
        num_segments = len(segments)
        num_cutout_segments = math.ceil(num_segments * self.fraction)
        cutout_segments = np.random.choice(a=range(0, num_segments), size=num_cutout_segments, replace=False)
        segments = np.delete(segments, cutout_segments)
        transformed_text = join_text_parts(segments)
        
        return transformed_text