from dataclasses import dataclass, field
from typing import List, Optional
from .parameter import Parameter


@dataclass
class Body:
    definitions: List[Parameter] = field(default_factory=list)
    calls: List[str] = field(default_factory=list)
    function_return: Optional[Parameter] = None

    def __repr__(self):
        return (
            f"declarations={self.definitions}, calls={self.calls}, "
            f"function return={self.function_return})"
        )
