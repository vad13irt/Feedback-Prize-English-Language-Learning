import numpy as np
from googletrans import Translator
from nltk.tokenize import sent_tokenize
from typing import List, Union, Tuple
from tqdm import tqdm
import random
import time


def translate_text(
    text: str, 
    translator: Translator, 
    source_language: str = "en", 
    target_language: str = "fr", 
    sentence_delay: float = 0.0, 
    max_length: int = 5000,
    ) -> str:
    
    def translate(text: str) -> str:
        return translator.translate(
            text=text, 
            src=source_language, 
            dest=target_language,
        ).text
    
    try:
        text = text.decode("utf-8")
    except AttributeError:
        text = text.encode("utf-8")
       
    text_length = len(text)
    if text_length >= max_length:
        sentences = sent_tokenize(text)
        translated_text = []
        for sentence in sentences:
            translated_sentence = translate(text=sentence)
            translated_text.append(translated_sentence)
            time.sleep(sentence_delay)
            
        translated_text = " ".join(translated_text)
    else:
        translated_text = translate(text=text)
        
    translated_text = translated_text.encode("utf-8")
    
    return translated_text


def translate_texts(texts: List[str], delay: float = 0.0, **kwargs) -> List[str]:
    translated_texts = []
    iterator = tqdm(texts, total=len(texts))
    for text in iterator:
        translated_text = translate_text(text=text, **kwargs)
        translated_texts.append(translated_text)
        time.sleep(delay)
    
    return translated_texts


def back_translate(
    texts: List[str], 
    translator: Translator, 
    source_language: str = "en", 
    target_language: str = "fr", 
    return_translated_texts: bool = False,
    delay_between_translations: float = 0.0,
    **kwargs,
    ) -> Union[List[str], Tuple[List[str], List[str]]]:
    
    translated_texts = translate_texts(
        texts=texts, 
        translator=translator, 
        source_language=source_language, 
        target_language=target_language, 
        **kwargs,
    )
    
    time.sleep(delay_between_translations)
    
    back_translated_texts = translate_texts(
        texts=translated_texts, 
        translator=translator, 
        source_language=target_language, 
        target_language=source_language, 
        **kwargs,
    )
    
    if return_translated_texts:
        return back_translated_texts, translated_texts
    
    return back_translated_texts


def __check_probabilitity(p: float) -> None:
    if not (0.0 <= p <= 1):
        raise ValueError(f"`p` must be in range [0, 1], but given {p}.")
    

def crop_text(
    text: str, 
    size: Tuple[int, int] = (1, 1), 
    min_sentences: int = 1, 
    p: float = 0.5,
    ) -> str:
    
    __check_probabilitity(p)
    
    if np.random.uniform() < p:
        sentences = sent_tokenize(text)
        num_sentences = len(sentences)
        index = random.randint(0 + min_sentences, num_sentences - 1 - min_sentences)
        
        left_width, right_width = size
        left_width, right_width = left_width + 1, right_width + 1
        left_index = min(0, index - left_width)
        right_index = min(index + right_width, num_sentences - 1)
        
        sentences = sentences[left_index:right_index]
        text = " ".join(sentences)
        
    return text


def remove_sentences_from_text(
    text: str, 
    num_sentences: int = 1, 
    p: float = 0.5,
    ) -> str:
    
    __check_probabilitity(p)
    
    if np.random.uniform() < p:
        sentences = sent_tokenize(text)
        num_sentences_ = len(sentences)
        
        if num_sentences_ > num_sentences:
            remove_indexes = np.random.choice(range(num_sentences_), size=num_sentences, replace=False)
            sentences = np.delete(sentences, remove_indexes)
            text = " ".join(sentences)
        else:
            text = ""
        
    return text