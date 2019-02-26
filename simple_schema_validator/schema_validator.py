from typing import Tuple, List, Dict, Any, Union, Deque, Optional

from collections import deque


MissingKeys = List[str]
AdditionalKeys = List[str]
Schema = Dict[str, Any]
Data = Dict[str, Any]

Paths = Dict[str, Optional[str]]  # item: parent


def build_path(item: str, parents: Paths) -> str:
    path: Deque[str] = deque()
    path.appendleft(item)

    while parents[item] is not None:
        path.appendleft(parents[item])  # type: ignore

        item = parents[item]  # type: ignore

    return '.'.join(path)


def build_paths(paths: Paths) -> List[str]:
    return [
        build_path(item, paths)
        for item in paths
    ]


def get_nested(d: Data, path: str) -> Any:
    parts = path.split('.')

    result = None

    for part in parts:
        result = d.get(part)

        if result is None:
            return None

        d = d[part]

    return result


def get_paths(d: Union[Data, Schema]) -> Paths:
    stack: Deque[Tuple[str, Optional[str]]] = deque()
    parents = {}  # item: parent, top-level items have None as parent

    for key in d:
        # Append a tuple of (item, parent)
        stack.append((key, None))

    while len(stack) > 0:
        item, parent = stack.pop()

        parents[item] = parent

        value = get_nested(d, build_path(item, parents))

        if type(value) is dict:
            for key in value:
                # Append a tuple of (item, parent)
                stack.append((key, item))

    return parents


class SchemaValidationResult:
    def __init__(self, *, valid, missing_keys, additional_keys, type_errors):
        self.__valid = valid
        self.__missing_keys = missing_keys
        self.__additional_keys = additional_keys
        self.__type_errors = type_errors

    @property
    def missing_keys(self):
        return self.__missing_keys

    @property
    def additional_keys(self):
        return self.__additional_keys

    @property
    def type_errors(self):
        return self.__type_errors

    def __bool__(self):
        return self.__valid


def schema_validator(schema: Schema, data: Data) -> SchemaValidationResult:
    schema_paths = set(build_paths(get_paths(schema)))
    data_paths = set(build_paths(get_paths(data)))

    missing_keys = schema_paths - data_paths
    additional_keys = data_paths - schema_paths

    return SchemaValidationResult(
        valid=schema_paths == data_paths,
        missing_keys=sorted(missing_keys),
        additional_keys=sorted(additional_keys),
        type_errors=[]
    )
