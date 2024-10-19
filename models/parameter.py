from dataclasses import dataclass
from typing import Optional


@dataclass
class Parameter:
    type: Optional[str] = None
    name: Optional[str] = None
    is_input: Optional[bool] = None

    def __eq__(self, other):
        if not isinstance(other, Parameter):
            return NotImplemented
        return (self.type == other.type) and (self.name == other.name)

    def __repr__(self):
        return f"{self.type} {self.name}"
