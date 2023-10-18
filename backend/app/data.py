from enum import Enum

class Source(Enum):
    quasarzone = "quasarzone"

    @property
    def hotdeal_id_header(self) -> str:
        hs = {
            "quasarzone": "QZ",
        }

        return hs[self.value]