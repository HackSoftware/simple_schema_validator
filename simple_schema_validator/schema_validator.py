from copy import deepcopy

from typing import Tuple, List, Dict, Any, Union, Deque, Optional

from operator import itemgetter

from collections import deque, Mapping


MissingKeys = List[str]
AdditionalKeys = List[str]
Schema = Dict[str, Any]
Data = Dict[str, Any]

Paths = Dict[str, Optional[str]]  # item: parent
OptionalPaths = List[str]


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


def set_nested(d: Data, path: str, value: Any) -> None:
    parts = path.split('.')

    last_part = parts[-1]

    for part in parts[:len(parts) - 1]:
        d = d[part]

    d[last_part] = value


def get_paths(d: Union[Data, Schema]) -> Tuple[Paths, OptionalPaths]:
    stack: Deque[Tuple[str, Optional[str]]] = deque()
    parents = {}  # item: parent, top-level items have None as parent
    optional_paths = []

    for key in d:
        # Append a tuple of (item, parent)
        stack.append((key, None))

    while len(stack) > 0:
        item, parent = stack.pop()

        parents[item] = parent

        path = build_path(item, parents)
        value = get_nested(d, path)

        if is_optional_schema(value):
            value = get_optional_type(value)

            set_nested(d, path, value)

            optional_paths.append(path)

        if type(value) is dict:
            for key in value:
                # Append a tuple of (item, parent)
                stack.append((key, item))

    return parents, optional_paths


class OptionalType:
    def __init__(self, T: Any):
        self.T = T


class OptionalTypeFactory:
    def __getitem__(self, T):
        return OptionalType(T)


def is_optional(t: Any) -> bool:
    return type(t) is OptionalType


def get_optional_type(t: OptionalType) -> Any:
    """
    If t is Optional[T], this function returns T

    Solution idea taken from this SO thread:
    https://stackoverflow.com/questions/46198178/unpack-optional-type-annotation-in-python-3-5-2

    """
    return t.T


def is_optional_schema(v: Any) -> bool:
    return is_optional(v) and isinstance(get_optional_type(v), Mapping)


class types:
    Optional = OptionalTypeFactory()


def type_check(schema, data, path, optional_paths) -> Tuple[bool, Optional[Dict[str, Any]]]:
    _type = get_nested(schema, path)
    value = get_nested(data, path)

    if isinstance(value, Mapping):
        return True, None

    if _type is Any:
        return True, None

    if _type is None:
        if value is None:
            return True, None

        return False, {'path': path, 'expected': None, 'actual': type(value)}

    if is_optional(_type):
        if value is None:
            return True, None

        _type = get_optional_type(_type)

    value_type = type(value)

    if value_type is _type:
        return True, None

    actual: Any = type(value)

    if value is None:
        if path in optional_paths:
            return True, None

        actual = None

    return False, {'path': path, 'expected': _type, 'actual': actual}


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


def remove_optional_values(data, optional_paths, schema_paths):
    paths_to_remove = set()

    for optional_path in optional_paths:
        value = get_nested(data, optional_path)

        if value is None:
            for schema_path in schema_paths:
                if schema_path != optional_path and schema_path.startswith(optional_path):
                    paths_to_remove.add(schema_path)

    return schema_paths - paths_to_remove


def schema_validator(schema: Schema, data: Data) -> SchemaValidationResult:
    schema = deepcopy(schema)

    schema_paths_mapping, optional_paths = get_paths(schema)
    data_paths_mapping, _ = get_paths(data)

    schema_paths = set(build_paths(schema_paths_mapping))
    data_paths = set(build_paths(data_paths_mapping))

    optional_paths = set(optional_paths)  # type: ignore

    schema_paths = remove_optional_values(data, optional_paths, schema_paths)

    missing_keys = schema_paths - data_paths
    additional_keys = data_paths - schema_paths

    existing_paths_in_schema = data_paths - additional_keys

    type_errors = []

    for path in existing_paths_in_schema:
        valid_type, type_error = type_check(schema, data, path, optional_paths)

        if not valid_type:
            type_errors.append(type_error)

    return SchemaValidationResult(
        valid=schema_paths == data_paths and not type_errors,
        missing_keys=sorted(missing_keys),
        additional_keys=sorted(additional_keys),
        type_errors=sorted(type_errors, key=itemgetter('path'))
    )
