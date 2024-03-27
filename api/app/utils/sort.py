from typing import List, Optional

from fastapi import Query

from models.sort import SortBy


def parse_sort(options: List[str]):
    async def _parse_sort(
        sort: Optional[str] = Query(None, regex=SortBy.create(options))
    ):
        if sort:
            return SortBy.parse(sort)

    return _parse_sort
