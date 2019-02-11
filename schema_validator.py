from collections import deque


def build_path(item, parents):
    path = deque()
    path.appendleft(item)

    while parents[item] is not None:
        path.appendleft(parents[item])

        item = parents[item]

    return '.'.join(path)


def get_nested(d, path):
    parts = path.split('.')

    result = None

    for part in parts:
        result = d.get(part)

        if result is None:
            return None

        d = d[part]

    return result


def get_paths(d):
    stack = deque()
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


def build_paths(paths):
    return [
        build_path(item, paths)
        for item in paths
    ]


def schema_validator(schema, data):
    schema_paths = set(build_paths(get_paths(schema)))
    data_paths = set(build_paths(get_paths(data)))

    missing_keys = schema_paths - data_paths
    additional_keys = data_paths - schema_paths

    return schema_paths == data_paths, missing_keys, additional_keys
