# analyzer/structures/function_structure.py
from dataclasses import dataclass, field
from typing import List, Optional
from .parameter import Parameter


@dataclass
class FuncStructure:
    type: str
    name: str
    parameters: List[Parameter] = field(default_factory=list)
    calls: List[str] = field(default_factory=list)
    # body: Optional[str] = None  # Substitua por c_ast.Compound ou outro tipo
    # ret: Optional[str] = None
    # is_called: List[str] = field(default_factory=list)

    def generate_func_signature(self) -> str:
        params = ", ".join([f"{param.type} {param.name}" for param in self.parameters])
        signature = f"{self.type} {self.name}({params})"
        return signature

    def __repr__(self):
        return (
            f"FuncStructure(type={self.type}, name={self.name}, parameters={self.parameters}, "
            f"calls={self.calls}, ret={self.ret})"
        )
