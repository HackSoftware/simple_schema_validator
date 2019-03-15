from typing import Any

from collections import Mapping


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

    """
    If the given value is another dictionary, don't type check.
    Consider this a valid type.
    """
    if isinstance(value, Mapping):
        return True, None

    """
    If type is Any, any we consider this a valid type.
    """
    if _type is Any:
        return True, None

    """
    If type is None, we check if the value is also None.
    """
    if _type is None:
        if value is None:
            return True, None

        return False, {'path': path, 'expected': None, 'actual': type(value)}

    """
    If type is types.Optional[T], we do the following:

    1) If value is None => valid.
    2) Otherwise, we say current type is T and continue.
    """
    if is_optional(_type):
        if value is None:
            return True, None

        _type = get_optional_type(_type)

    """
    Straight-forward case.
    We take the type of the value and compare.
    """
    value_type = type(value)

    if value_type is _type:
        return True, None

    """
    If value is None but the path is in the optional paths,
    we consider this valid.

    Otherwise we fail with the actual type of the value.
    """
    actual = value_type

    if value is None:
        if path in optional_paths:
            return True, None

        actual = None

    return False, {'path': path, 'expected': _type, 'actual': actual}
