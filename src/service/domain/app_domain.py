from typing import Optional

class AppDomain:
    id: Optional[int]
    name: str
    description: str

    def __init__(self, name: str, description: str, id: Optional[int] = None):
        self.id = id
        self.name = name
        self.description = description

    @classmethod
    def build(cls, name: str, description: str, id: Optional[int] = None):
        return cls(name=name, description=description, id=id)