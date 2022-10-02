from transform import Transform
from typing import List, Union


class Compose:
    def __init__(self, transforms: List[Transform]) -> None:
        self.transforms = transforms
    
    def __call__(self, text: Union[str, List[str]]):
        for transform in self.transforms:
            text = transform(text)
        
        return text