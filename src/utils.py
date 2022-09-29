import numpy as np
from typing import List
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