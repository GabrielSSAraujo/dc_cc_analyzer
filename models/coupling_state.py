from dataclasses import dataclass, field
from typing import Optional, List
from .parameter import Parameter
from enum import Enum


class StateOnDest(Enum):
    R = 0
    M = 1


@dataclass
class CouplingState:
    parameter: Optional[Parameter] = None
    origin: Optional[str] = None
    destination: Optional[str] = None
    state_on_dest: Optional[StateOnDest] = None

    def __repr__(self):
        return f"origin: {self.origin}, destination: {self.destination}, use: {self.state_on_dest}"
