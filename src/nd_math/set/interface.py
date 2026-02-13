from typing import Any, runtime_checkable, Protocol


@runtime_checkable
class Interface(Protocol):
    _members: Any
    def __init__(self, _members:Any):
        ...

