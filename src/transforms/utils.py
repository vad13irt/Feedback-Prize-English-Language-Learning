from typing import Optional, Union, Iterable, List
import string


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
        part = str(part)
        sep = " " if part[0] not in punctuations else ""  
        text += sep + part
    
    text = text.strip()
    
    return text