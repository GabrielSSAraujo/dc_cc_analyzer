from dataclasses import dataclass, field
from typing import Optional, List
from .parameter import Parameter


@dataclass
class FunctionInterface:
    function_name: Optional[str] = None
    input_parameters: List[Parameter] = field(default_factory=list)
    output_parameters: List[Parameter] = field(default_factory=list)

    def __repr__(self):
        return f"name:{self.function_name}, input_parameters:{self.input_parameters}, output_parameters:{self.output_parameters}"
