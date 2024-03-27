from typing import List, Optional
from pydantic import BaseModel
from enum import StrEnum, auto


class SortOption(StrEnum):
    desc = auto()
    asc = auto()
    NONE = auto()


class SortBy(BaseModel):

    name: str
    by: SortOption

    @staticmethod
    def create(options: List[str]) -> str:
        return "|".join(f"^{opt}$|^{opt}\:asc$|^{opt}\:desc$" for opt in options)

    @staticmethod
    def parse(value: str) -> "SortBy":
        vals = value.split(":", 1)
        return SortBy(name=vals[0], by=vals[1:] or SortOption.NONE)
