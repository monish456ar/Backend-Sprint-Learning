


from typing import Callable, Final, Generic, Protocol, TypeVar, TypedDict


T = TypeVar("T")
U = TypeVar("U")
K = TypeVar("K")


MAX_PIPELINE_ITEMS: Final[int] = 1000


class RecordValidator(Protocol[T]):
    def validate(self, item: T) -> bool:
        ...


class PipelineConfig(TypedDict):
    name: str
    enabled: bool
    batch_size: int


class Pipeline(Generic[T]):
    def __init__(self, items: list[T]):
        self.items = items

    def filter(self, condition: Callable[[T], bool]) -> list[T]:
        return [item for item in self.items if condition(item)]

    def transform(self, transform_fn: Callable[[T], U]) -> list[U]:
        return [transform_fn(item) for item in self.items]

    def group_by(self, key_fn: Callable[[T], K]) -> dict[K, list[T]]:
        groups: dict[K, list[T]] = {}

        for item in self.items:
            key = key_fn(item)

            if key not in groups:
                groups[key] = []

            groups[key].append(item)

        return groups


def validate_records(
    items: list[T],
    validator: RecordValidator[T],
) -> list[T]:
    return [
        item for item in items
        if validator.validate(item)
    ]


