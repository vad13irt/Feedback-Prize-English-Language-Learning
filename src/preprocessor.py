from flashtext import KeywordProcessor
from collections import Iterable
from typing import Union, List
import contractions


class Preprocessor:
    def __init__(self) -> None:
        contractions_dict = contractions.contractions_dict
        contractions_dict.update(contractions.slang_dict)
        
        reversed_contractions_dict = {v: k for k, v in contractions_dict.items()}
        
        self.contractions_dict = {k: [v] for k, v in contractions_dict.items()}
        self.reversed_contractions_dict = {k: [v] for k, v in reversed_contractions_dict.items()}
        
        self.keyword_processor = KeywordProcessor()
        self.keyword_processor.add_keywords_from_dict(self.reversed_contractions_dict)
        
    def preprocess(self, text: str) -> str:
        text = self.keyword_processor.replace_keywords(text)
        
        return text
        
    def __call__(self, text: Union[str, List[str]]) -> Union[str, List[str]]:
        if isinstance(text, str):
            preprocessed_text = self.preprocess(text)
        elif isinstance(text, Iterable):
            preprocessed_text = [self.preprocess(t) for t in text]
            
        return preprocessed_text