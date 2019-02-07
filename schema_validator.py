from collections import deque


def _build_path(item, parents):
    path = deque()
    path.appendleft(item)

    while parents[item] is not None:
        path.appendleft(parents[item])  # [b, ]

        item = parents[item]

    return '.'.join(path)


def _get_nested(d, path):
    parts = path.split('.')

    result = None

    for part in parts:
        result = d.get(part)

        if result is None:
            return None

        d = d[part]

    return result


def _get_paths(d):
    stack = deque()
    parents = {}  # item: parent, top-level items have None as parent

    for key in d:
        # Append a tuple of (item, parent)
        stack.append((key, None))

    while len(stack) > 0:
        item, parent = stack.pop()

        parents[item] = parent

        value = _get_nested(d, _build_path(item, parents))

        if type(value) is dict:
            for key in value:
                # Append a tuple of (item, parent)
                stack.append((key, item))

    return parents


def _add_to_keys(keys, key, key_depth=None):
    missing_key = key
    if key_depth:
        missing_key = f'{".".join(key_depth)}.{key}'

    keys.append(missing_key)
    return keys


def schema_validator(schema, data):
    parents = _get_paths(data)

    def internal(schema, data, missing_keys=None, additional_keys=None, key_depth=None):
        used_keys = set()
        all_keys = set(data.keys())

        if missing_keys is None:
            missing_keys = []

        if additional_keys is None:
            additional_keys = []

        if key_depth is None:
            key_depth = []

        for element in schema:
            if type(element) is list:
                key, nested_schema = element
                used_keys.add(key)

                if key in data:
                    key_depth.append(key)

                    valid, missing_keys, additional_keys = internal(
                        nested_schema,
                        data[key],
                        missing_keys,
                        additional_keys,
                        key_depth=key_depth
                    )

                    key_depth.clear()
                else:
                    missing_keys = _add_to_keys(missing_keys, key, key_depth)
            else:
                used_keys.add(element)

                if element not in data:
                    missing_keys = _add_to_keys(missing_keys, element, key_depth)

        additional_keys += [_build_path(x, parents) for x in all_keys if x not in used_keys]

        return additional_keys == [] and missing_keys == [], missing_keys, additional_keys

    return internal(schema, data)


if __name__ == '__main__':
    schema = [
        'a',
        'b',
        [
            'c',
            [['d', [['e', ['g', 'h']]]]]
        ],
        'r',
        [
            'l', ['a', 'b']
        ]
    ]

    data = {
            'a': 1,
            'b': 2,
            'c': {
                'd': {
                    'f': 3,
                    'e': {
                        'g': 2,
                        'i': 23
                    }
                }
            },
            'l': {
                'a': 2,
                'h': 34
            }
        }

    print(schema_validator(schema, data))
