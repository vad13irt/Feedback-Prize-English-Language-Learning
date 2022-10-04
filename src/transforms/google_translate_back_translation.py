from transform import Transform
from utils import join_text_parts
from googletrans import Translator
from typing import List, Union, Optional
from collections import Iterable
from nltk.tokenize import sent_tokenize
from argparse import ArgumentParser
from tqdm import tqdm
import pandas as pd
import time

import nltk
nltk.download('punkt')


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
            for t in tqdm(text, total=len(text)):
                transformed_t = self.apply(t)
                transformed_text.append(transformed_t)
                time.sleep(self.delay)
        else:
            transformed_text = text
        
        return transformed_text


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--data_frame_path", required=True)
    parser.add_argument("--source_language", required=True)
    parser.add_argument("--target_language", required=True)
    parser.add_argument("--output_path", required=True)
    parser.add_argument("--text_column", required=False, default="text")
    parser.add_argument("--back_translated_column", required=False, default="back_translated_text")

    args, unknown_args = parser.parse_known_args()

    back_translation = GoogleTranslateBackTranslation(
        source_language=args.source_language, 
        target_language=args.target_language,
        p=1.0,
        **dict(unknown_args),
    )
    
    data_frame = pd.read_csv(args.data_frame_path)
    texts = data_frame[args.text_column].values

    print(f"Back-translation '{args.source_language}' -> '{args.target_language}' -> '{args.source_language}' of {len(texts)} texts")
    
    data_frame[args.back_translated_column] = back_translation(texts)
    data_frame.to_csv(args.output_path, index=False)
    
    print(f"Back-translated texts were saved to '{args.output_path}'")
