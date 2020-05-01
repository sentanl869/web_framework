from enum import (
    Enum,
    auto,
)


class UserRole(Enum):
    guest = auto()
    normal = auto()
    admin = auto()

    def translate(self, _escape_table) -> str:
        return self.name
