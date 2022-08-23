import uuid
import time
from typing import (
    Any,
    Dict
)


class ObjectDict(Dict[str, Any]):
    """Makes a dictionary behave like an object, with attribute-style access.
    """

    def __getattr__(self, name: str) -> Any:
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name: str, value: Any) -> None:
        self[name] = value


def generate_guid(prefix=''):
    return str(uuid.uuid3(uuid.NAMESPACE_URL, prefix + str(time.time())))
