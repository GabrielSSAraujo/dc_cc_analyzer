from dataclasses import dataclass, field
from typing import Optional, List
from .parameter import Parameter


@dataclass
class Coupling:
    function_a: Optional[str] = None
    function_b: Optional[str] = None
    parameters: List[Parameter] = field(default_factory=list)

    def __eq__(self, coupling):
        return (coupling.function_a == self.function_a) and (
            coupling.function_b == self.function_b
        )

    def __repr__(self):
        return f"{self.function_a} -> {self.function_b} -> {self.parameters}"
