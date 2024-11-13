from dataclasses import dataclass, field
from typing import Optional, List
from .parameter import Parameter


@dataclass
class Coupling:
    function_a: Optional[str] = None
    function_b: Optional[str] = None
    coord_a: List[int] = field(default_factory=list)
    coord_b: List[int] = field(default_factory=list)
    parameters: List[Parameter] = field(default_factory=list)

    def __repr__(self):
        return f"{self.function_a} -> {self.function_b} : {self.coord_a}, {self.coord_b} -> {self.parameters}"
