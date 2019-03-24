from typing import Any

from collections import deque

from .schema_types import is_optional_schema, get_optional_type, is_any_or_optional_any


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


def set_nested(d, path: str, value: Any) -> None:
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


def get_paths_with_any(schema_paths_mapping):
    return set(path for path, _type in schema_paths_mapping.items() if is_any_or_optional_any(_type))
