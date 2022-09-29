from collections import Iterable
from typing import Union, List
import pandas as pd
import numpy as np
import copy


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