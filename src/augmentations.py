from googletrans import Translator
from nltk.tokenize import sent_tokenize
from typing import List
from tqdm import tqdm
import time


def translate_text(
    text: str, 
    translator: Translator, 
    source_language: str = "en", 
    translate_language: str = "fr", 
    sentence_delay: int = 0, 
    max_length: int = 5000,
    ) -> str:
    
    def translate(text: str) -> str:
        return translator.translate(
            text=text, 
            src=source_language, 
            dest=translate_language,
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
            time.sleep(sentence_delay)
            
        translated_text = " ".join(translated_text)
    else:
        translated_text = translate(text=text)
        
    translated_text = translated_text.encode("utf-8")
    
    return translated_text


def translate_texts(texts: List[str], delay: int = 0, **kwargs) -> List[str]:
    translated_texts = []
    iterator = tqdm(enumerate(texts), total=len(texts))
    for index, text in iterator:
        translated_text = translate_text(text=text, **kwargs)
        translated_texts.append(translated_text)
        time.sleep(delay)
    
    return translated_texts


def back_translate(
    texts: List[str], 
    translator: Translator, 
    source_language: str = "en", 
    translate_language: str = "fr", 
    return_translated_texts: bool = False,
    **kwargs,
    ) -> List[str]:
    
    translated_texts = translate_texts(
        texts=texts, 
        translator=translator, 
        source_language=source_language, 
        translate_language=translate_language, 
        **kwargs,
    )

    back_translated_texts = translate_texts(
        texts=translated_texts, 
        translator=translator, 
        source_language=translate_language, 
        translate_language=source_language, 
        **kwargs,
    )
    
    if return_translated_texts:
        return back_translated_texts, translated_texts
    
    return back_translated_texts