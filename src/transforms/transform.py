import numpy as np
from collections import Iterable
from typing import List, Union
from tqdm import tqdm


class Transform:
    def __init__(self, p: float = 0.5) -> None:
        self.p = p
        
        if not (0.0 <= self.p <= 1):
            raise ValueError(f"`p` must be in range [0, 1], but given {self.p}")
           
    def apply(self, text: str) -> str:
        if np.random.uniform() < self.p:
            text = self.transform(text)
        
        return text
            
    def transform(self, text: str) -> str:
        return text
    
    def __call__(self, text: Union[str, List[str]]) -> Union[str, List[str]]:
        if isinstance(text, str):
            transformed_text = self.apply(text)
        elif isinstance(text, Iterable):
            transformed_text = [self.apply(t) for t in tqdm(text, total=len(text))]
        else:
            transformed_text = text
        
        return transformed_text