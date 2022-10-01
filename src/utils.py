import pandas as pd
import numpy as np
from collections import Iterable
from typing import List, Tuple, Dict, Any, Union
import json
import copy
import re


def convert_soft_to_hard_predictions(
    soft_predictions: np.ndarray, 
    bins: List[float] = [0.0, 0.25, 0.75, 1.25, 1.75, 2.25, 2.75, 3.25, 3.75, 4.25, 4.75], 
    labels: List[float] = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0],
) -> np.ndarray:

    soft_predictions = np.clip(soft_predictions, a_min=0.0, a_max=5.0)
    hard_predictions = np.digitize(soft_predictions, bins=bins, right=True)
    hard_predictions = [labels[hard_prediction - 1] for hard_prediction in hard_predictions]
    
    return hard_predictions


def get_private_values(text: str, pattern: str = "(Generic_[a-zA-Z]\w+)|((\w+[A-Z]_\w+))") -> List[str]:
    private_values_list = re.findall(pattern, text)
    private_values = []
    for private_value in private_values_list:
        if len(private_value) > 0:
            private_value = [value for value in private_value if value != ""]
            private_values.extend(private_value)
    
    private_values = list(set(private_values))
    return private_values

def preprocess_private_values(text: str) -> str:
    replace_private_values = {
        "Generic_Namehad": "Generic_Name had",
        "PROEPR_NAME": "PROPER_NAME",
        "Generic_school": "Generic_School",
        "Generic_Citynbsp": "Generic_City nbsp",
        "Generic_Namea": "Generic_Name a",
    }
    
    for private_value, replace_value in replace_private_values.items():
        text = text.replace(private_value, replace_value)
        
    return text

def get_private_values(text: str, pattern: str = "(Generic_[a-zA-Z]\w+)|((\w+[A-Z]_\w+))") -> List[str]:
    private_values_list = re.findall(pattern, text)
    private_values = []
    for private_value in private_values_list:
        if len(private_value) > 0:
            private_value = [value for value in private_value if value != ""]
            private_values.extend(private_value)
    
    private_values = list(set(private_values))
    
    return private_values

def preprocess_private_values(text: str) -> str:
    replace_private_values = {
        "Generic_Namehad": "Generic_Name had",
        "PROEPR_NAME": "PROPER_NAME",
        "Generic_school": "Generic_School",
        "Generic_Citynbsp": "Generic_City",
        "Generic_Namea": "Generic_Name a",
    }
    
    for private_value, replace_value in replace_private_values.items():
        text = text.replace(private_value, replace_value)
        
    return text


def preprocess_languages(languages: List[Tuple[str, str]]) -> List[str]:
    """
    Languages source: https://gist.github.com/alexanderjulo/4073388
    """
    
    languages = [language for (code, language) in languages]
    
    new_languages = []
    for language in languages:
        if ";" in language:
            language = [lang.strip() for lang in language.split(";")]
            new_languages.extend(language)
        else:
            new_languages.append(language)
    
    languages = [re.sub("[\(\[].*?[\)\]]", "", language) for language in new_languages]
    languages = list(set(languages))
    
    return languages


def create_adult_name(name: str, male: bool = True):
    appeal = "Mr." if male else "Mrs."

    return f"{appeal} {name}"


def char_range(c1, c2):
    """Generates the characters from `c1` to `c2`, inclusive."""
    for c in range(ord(c1), ord(c2)+1):
        yield chr(c)
        

def write_json(data: Dict[str, Any], path: str, mode: str = "w", **kwargs) -> None:
    with open(path, mode=mode, **kwargs) as file:
        data = json.dumps(data)
        file.write(data)
        
def read_json(path: str, mode: str = "r", **kwargs) -> Dict[str, Any]:
    with open(path, mode=mode, **kwargs) as file:
        data = file.read()
        data = json.loads(data)
    
    return data

def basic_selection(
    data_frame: pd.DataFrame, 
    min_words: int = 150, 
    max_words: int = 1700, 
    types: Union[str, List[str]] = "Essay",
    text_column: str = "full_text",
    type_column: str = "type", 
    drop_extra_columns: bool = True,
) -> pd.DataFrame:
    
    data_frame = copy.deepcopy(data_frame)
        
    # length selection
    data_frame["num_words"] = data_frame[text_column].apply(lambda text: len(str(text).split()))
    words_threshold_mask = (min_words < data_frame["num_words"]) & (data_frame["num_words"] < max_words)
    data_frame = data_frame[words_threshold_mask]
    
    # type selection
    if isinstance(types, str):
        types_mask = data_frame[type_column].str.contains(types)
    elif isinstance(types, Iterable):
        types_mask = data_frame[type_column].isin(types)
    else:
        types_mask = np.ones(shape=data_frame.shape[0], dtype=bool)
    
    na_types_mask = data_frame[type_column].isna()
    
    selected_data_mask = na_types_mask | types_mask
    data_frame = data_frame[selected_data_mask]
    
    # removing duplicates
    data_frame = data_frame.drop_duplicates(subset=["full_text"])
    
    # dropping extra columns
    if drop_extra_columns:
        extra_columns = ["num_words"]
        data_frame = data_frame.drop(extra_columns, axis=1)
    
    return data_frame