# analyzer/structures/parameter.py
from dataclasses import dataclass, field
from typing import Optional, List
from .parameter import Parameter


@dataclass
class CouplingList:
    function_a: Optional[str] = None
    function_b: Optional[str] = None
    coupled_parameters: List[Parameter] = field(default_factory=list)

    def __repr__(self):
        return f"{self.function_a} -> {self.function_a} : {self.coupled_parameters}"
