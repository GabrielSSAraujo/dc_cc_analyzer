from dataclasses import dataclass
from typing import Optional
import copy

@dataclass
class Parameter:
    type: Optional[str] = None
    name: Optional[str] = None
    current_name: Optional[str] = None
    pointer_depth: Optional[str] = None

    def clone(self):
        return copy.deepcopy(self)

    def __eq__(self, other):
        if not isinstance(other, Parameter):
            return NotImplemented
        return (self.type == other.type) and (self.name == other.name)

    def __repr__(self):
        return f"{self.type} {self.pointer_depth}{self.name}"
