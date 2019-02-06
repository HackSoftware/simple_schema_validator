def add_to_missing_keys(missing_keys, key, given_key=None):
    missing_key = key
    if given_key:
        missing_key = f'{given_key}.{key}'

    missing_keys.append(missing_key)
    return missing_keys


def schema_validator(schema, data, missing_keys=None, additional_keys=None, given_key=None):
    used_keys = set()
    all_keys = set(data.keys())

    if missing_keys is None:
        missing_keys = []

    if additional_keys is None:
        additional_keys = []

    for element in schema:
        if type(element) is list:
            key, nested_schema = element
            used_keys.add(key)
            if key in data:
                missing_keys, additional_keys = schema_validator(
                    nested_schema,
                    data[key],
                    missing_keys,
                    additional_keys,
                    given_key=key
                )
            else:
                missing_keys = add_to_missing_keys(missing_keys, key, given_key)
        else:
            used_keys.add(element)

            if element not in data:
                missing_keys = add_to_missing_keys(missing_keys, element, given_key)

    additional_keys += [x for x in all_keys if x not in used_keys]

    return missing_keys, additional_keys


if __name__ == '__main__':
    schema = [
        'a',
        'b',
        [
            'c',
            [['d', ['e']]]
        ]
    ]

    data = {
            'a': 1,
            'b': 2,
            'c': {
                'd': {
                    'f': 3
                }
            }
        }

    print(schema_validator(schema, data))
