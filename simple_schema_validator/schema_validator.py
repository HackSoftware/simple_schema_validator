from copy import deepcopy

from typing import List, Dict, Any, Optional

from operator import itemgetter

from collections import deque, Mapping


MissingKeys = List[str]
AdditionalKeys = List[str]
Schema = Dict[str, Any]
Data = Dict[str, Any]

Paths = Dict[str, Optional[str]]  # item: parent
OptionalPaths = List[str]


def get_paths(d):
    stack = deque()
    parents = {}  # item: parent, top-level items have None as parent
    paths = {}

    for key, value in d.items():
        # Append a tuple of (item, parent, value, path)
        stack.append((key, None, value, [key]))

    while len(stack) > 0:
        item, parent, value, path = stack.pop()

        parents[item] = parent
        paths['.'.join(path)] = value

        if type(value) is dict:
            for key, new_value in value.items():
                # Append a tuple of (item, parent)
                stack.append((key, item, new_value, [p for p in path] + [key]))

    return paths


def set_nested(d: Data, path: str, value: Any) -> None:
    parts = path.split('.')

    last_part = parts[-1]

    for part in parts[:len(parts) - 1]:
        d = d[part]

    d[last_part] = value


def replace_optional_schema_paths(schema):
    stack = deque()
    optional_paths = []

    for key, value in schema.items():
        # Append a tuple of (item, value, path)
        stack.append((key, value, [key]))

    while len(stack) > 0:
        item, value, path = stack.pop()

        if is_optional_schema(value):
            value = get_optional_type(value)

            set_nested(schema, '.'.join(path), value)

            optional_paths.append('.'.join(path))

        if type(value) is dict:
            for key, new_value in value.items():
                # Append a tuple of (item, parent)
                stack.append((key, new_value, [p for p in path] + [key]))

    return get_paths(schema), optional_paths


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


def type_check(schema_paths_mapping, data_paths_mapping, path, optional_paths):
    _type = schema_paths_mapping.get(path)
    value = data_paths_mapping.get(path)

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


def remove_optional_values(data_paths_mapping, optional_paths, schema_paths):
    paths_to_remove = set()

    for optional_path in optional_paths:
        value = data_paths_mapping.get(optional_path, None)

        if value is None:
            for schema_path in schema_paths:
                if schema_path != optional_path and schema_path.startswith(optional_path):
                    paths_to_remove.add(schema_path)

    return schema_paths - paths_to_remove


def schema_validator(schema: Schema, data: Data) -> SchemaValidationResult:
    schema = deepcopy(schema)

    schema_paths_mapping, optional_paths = replace_optional_schema_paths(schema)
    data_paths_mapping = get_paths(data)

    schema_paths = set(schema_paths_mapping)
    data_paths = set(data_paths_mapping)

    optional_paths = set(optional_paths)

    schema_paths = remove_optional_values(data_paths_mapping, optional_paths, schema_paths)

    missing_keys = schema_paths - data_paths
    additional_keys = data_paths - schema_paths

    existing_paths_in_schema = data_paths - additional_keys

    type_errors = []

    for path in existing_paths_in_schema:
        valid_type, type_error = type_check(
            schema_paths_mapping,
            data_paths_mapping,
            path,
            optional_paths
        )

        if not valid_type:
            type_errors.append(type_error)

    return SchemaValidationResult(
        valid=schema_paths == data_paths and not type_errors,
        missing_keys=sorted(missing_keys),
        additional_keys=sorted(additional_keys),
        type_errors=sorted(type_errors, key=itemgetter('path'))
    )
