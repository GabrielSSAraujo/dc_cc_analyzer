from dataclasses import dataclass, field
from typing import List, Optional
from .parameter import Parameter
from .function_body import Body


@dataclass
class FuncStructure:
    type: str
    name: str
    pointer_depth: Optional[str]
    parameters: List[Parameter] = field(default_factory=list)
    body: Optional[Body] = field(default_factory=Body)

    def generate_func_signature(self) -> str:
        params = ", ".join([f"{param.type} {param.name}" for param in self.parameters])
        signature = f"{self.type} {self.pointer_depth}{self.name}({params})"
        return signature

    def __repr__(self):
        return (
            f"FuncStructure(type={self.type}, name={self.pointer_depth}{self.name}, parameters={self.parameters}, "
            f"body={self.body})"
        )
