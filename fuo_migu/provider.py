from fuocore.provider import AbstractProvider  # noqa

from fuo_migu import __alias__, __identifier__


class MiguProvider(AbstractProvider):
    def __init__(self):
        super().__init__()

    @property
    def name(self) -> str:
        return __alias__

    @property
    def identifier(self) -> str:
        return __identifier__


provider = MiguProvider()
from fuo_migu.models import search

provider.search = search
