def _add_to_missing_keys(missing_keys, key, key_depth=None):
    missing_key = key
    if key_depth:
        missing_key = f'{".".join(key_depth)}.{key}'

    missing_keys.append(missing_key)
    return missing_keys


def schema_validator(schema, data):
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

                    missing_keys, additional_keys = internal(
                        nested_schema,
                        data[key],
                        missing_keys,
                        additional_keys,
                        key_depth=key_depth
                    )

                    key_depth.clear()
                else:
                    missing_keys = _add_to_missing_keys(missing_keys, key, key_depth)
            else:
                used_keys.add(element)

                if element not in data:
                    missing_keys = _add_to_missing_keys(missing_keys, element, key_depth)

        additional_keys += [x for x in all_keys if x not in used_keys]

        return missing_keys, additional_keys

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
                        'g': 2
                    }
                }
            },
            'l': {
                'a': 2
            }
        }

    print(schema_validator(schema, data))
