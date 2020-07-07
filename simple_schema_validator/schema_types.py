from typing import Any, List

from collections.abc import Mapping


class OptionalType:
    def __init__(self, T: Any):
        self.T = T


class OptionalTypeFactory:
    def __getitem__(self, T):
        return OptionalType(T)


class ListType:
    def __init__(self, T: Any):
        self.T = T


class ListTypeFactory:
    def __getitem__(self, T):
        return ListType(T)


def is_optional(t: Any) -> bool:
    return type(t) is OptionalType


def get_optional_type(t: OptionalType) -> Any:
    """
    If t is Optional[T], this function returns T

    Solution idea taken from this SO thread:
    https://stackoverflow.com/questions/46198178/unpack-optional-type-annotation-in-python-3-5-2

    """
    return t.T


def get_listType_type(t: ListType) -> Any:
    return t.T


def is_optional_schema(v: Any) -> bool:
    return is_optional(v) and isinstance(get_optional_type(v), Mapping)


def is_any(v: Any) -> bool:
    return v is Any


def is_any_or_optional_any(v: Any) -> bool:
    return is_any(v) or (is_optional(v) and is_any(get_optional_type(v)))


def is_list(v: Any) -> bool:
    return type(v) is list


def is_dict(v: Any) -> bool:
    return type(v) is dict


def get_list_type(v: Any) -> Any:
    try:
        if len(v) > 0:
            return v[0]
    except TypeError:
        return get_listType_type(v)

    return Any


def get_expected_type(v: Any) -> type:
    if is_list(v):
        return list

    return v


class types:
    Optional = OptionalTypeFactory()
    List = ListTypeFactory()


def type_check_lists(_type, value, path):
    errors = []

    list_type = get_list_type(_type)

    for index, item in enumerate(value):
        if is_any(list_type):
            continue

        if is_dict(list_type):
            from .schema_validator import schema_validator
            validate = schema_validator(list_type, item)

            if not bool(validate):
                for error in validate.type_errors:
                    errors.append(error)

            continue

        if type(item) is not list_type:
            errors.append({
                'path': f'{path}[{index}]',
                'expected': list_type,
                'actual': type(item)
            })

    if errors:
        return False, errors

    return True, None


def type_check(schema_paths_mapping, data_paths_mapping, path, optional_paths):
    _type = schema_paths_mapping.get(path)
    value = data_paths_mapping.get(path)

    """
    If the given value is another dictionary, don't type check.
    Consider this a valid type.
    """
    if isinstance(value, Mapping):
        if type(_type) is not type(value):
            if not is_optional(_type) and not is_any_or_optional_any(_type):
                return False, [{'path': path, 'expected': type(_type), 'actual': type(value)}]

            if is_optional(_type):
                optional_type = get_optional_type(_type)

                if type(optional_type) is not type and not is_any_or_optional_any(optional_type):
                    return False, [{'path': path, 'expected': type(optional_type), 'actual': type(value)}]

        return True, None

    """
    If type is any, we consider this a valid type.
    """
    if is_any(_type):
        return True, None

    """
    If type is None, we check if the value is also None.
    """
    if _type is None:
        if value is None:
            return True, None

        return False, [{'path': path, 'expected': None, 'actual': type(value)}]

    """
    If type is types.Optional[T], we do the following:

    1) If value is None => valid.
    2) Otherwise, we say current type is T and continue.
    """
    if is_optional(_type):
        if value is None:
            return True, None

        _type = get_optional_type(_type)

    if is_list(value):
        type_check_lists_result = type_check_lists(_type, value, path)

        if type_check_lists_result is not None:
            return type_check_lists_result

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

    return False, [{'path': path, 'expected': get_expected_type(_type), 'actual': actual}]
