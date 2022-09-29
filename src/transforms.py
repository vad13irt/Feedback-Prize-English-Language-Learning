from googletrans import Translator
from typing import List, Union, Optional, Dict
from collections import Iterable
from nltk.tokenize import sent_tokenize, word_tokenize
from num2words import num2words
import contractions
import numpy as np
import requests
import random
import string
import math
import json
import time
import re


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
            transformed_text = [self.apply(t) for t in text]
        else:
            transformed_text = text
        
        return transformed_text


class Compose:
    def __init__(self, transforms: List[Transform]) -> None:
        self.transforms = transforms
    
    def __call__(self, text: Union[str, List[str]]):
        for transform in self.transforms:
            text = transform(text)
        
        return text


class GoogleTranslateBackTranslation(Transform):
    def __init__(
        self, 
        translator: Optional[Translator] = None, 
        source_language: str = "en", 
        target_language: str = "fr", 
        delay: float = 1.0, 
        segment_delay: float = 1.0,
        translations_delay: float = 1.0,
        max_length: int = 5000,
        p: float = 0.5,
        **translator_args,
    ) -> None:
        super().__init__(p)    
    
        self.translator = translator
        self.source_language = source_language
        self.target_language = target_language
        self.delay = delay
        self.segment_delay = segment_delay
        self.translations_delay = translations_delay
        self.max_length = max_length
        self.translator_args = translator_args

        if self.translator is None:
            self.translator = Translator(**self.translator_args)

        self.translate_func = lambda text, source_language, target_language: self.translator.translate(
            text=text, 
            src=source_language, 
            dest=target_language,
        ).text
        
    def split_text_into_segments(self, text: str) -> List[str]:        
        return sent_tokenize(text)
        
    def translate(self, text: str, source_language: str, target_language: str) -> str:        
        text_length = len(text)
        if text_length >= self.max_length:
            translated_text = []
            segments = self.split_text_into_segments(text)
            for segment in segments:
                translated_segment = self.translate_func(
                    text=segment, 
                    source_language=source_language, 
                    target_language=target_language,
                )
                
                translated_text.append(translated_segment)
                time.sleep(self.segment_delay)
            
            translated_text = join_text_parts(translated_text)
        else:
            translated_text = self.translate_func(
                text=text, 
                source_language=source_language, 
                target_language=target_language,
            )
            
        return translated_text
        
    def transform(self, text: str, return_translated_text: bool = False) -> str:
        translated_text = self.translate(
            text=text, 
            source_language=self.source_language, 
            target_language=self.target_language,
        )
        
        time.sleep(self.translations_delay)
        
        back_translated_text = self.translate(
            text=translated_text, 
            source_language=self.target_language, 
            target_language=self.source_language,
        )
        
        if return_translated_text:
            return back_translated_text, translated_text
        
        return back_translated_text
    
    
    def __call__(self, text: Union[str, List[str]]) -> Union[str, List[str]]:
        if isinstance(text, str):
            transformed_text = self.apply(text)
        elif isinstance(text, Iterable):
            transformed_text = []
            for t in text:
                transformed_t = self.apply(t)
                transformed_text.append(transformed_t)
                time.sleep(self.delay)
        else:
            transformed_text = text
        
        return transformed_text


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


class NumberToWords(Transform):      
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
                if word.isdigit() and (np.random.uniform() < self.p or self.level == "text"):
                    word = num2words(int(word))
                    
                new_words.append(word)
            
            text = join_text_parts(new_words)
            
        return text    


class Accent(Transform):
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

class SlangConverter(Transform):
    def __init__(
        self, 
        level: str = "text",
        slang_dict: Optional[Dict[str, str]] = None, 
        punctuations: str = ".,:?! ", 
        p: float = 0.5,
    ):
        super().__init__(p)
        
        self.slang_dict = slang_dict
        self.level = level
        self.punctuations = punctuations
        
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
                
            if full in text and not transformed and does_apply:
                func = lambda match: self.replace_function(match, data=self.reversed_slang_dict)
                text = re.sub(f"[{self.punctuations}]{full}[{self.punctuations}]", func, text)
    
        return text


class KeywordReplacer(Transform):
    def __init__(
        self, 
        keywords: Optional[Dict[str, List[str]]],
        level: str = "text", 
        p: float = 0.5, 
        **keyword_processor_args,
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


def join_text_parts(parts: List[str], punctuations: Optional[Union[Iterable, str]] = None) -> str:
    """
    Smart join of text's parts
    
    Basic join: ['It', "'s", "example", "!"] -> "It 's example !"
    Smart join: ['It', "'s", "example", "!"] -> "It's example!"
    """
    
    if punctuations is None:
        punctuations = string.punctuation 
    
    text = ""
    for part in parts:
        sep = " "
        if part[0] in punctuations:
            sep = ""
            
        text += sep + part
    
    text = text.strip()
    
    return text