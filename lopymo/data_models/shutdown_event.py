from dataclasses import dataclass


@dataclass
class ShutdownEvent:
    reason: str = ''
