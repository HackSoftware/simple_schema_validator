def schema_validator(schema, data, missing_keys=None, additional_keys=None):
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
                    additional_keys
                )
            else:
                missing_keys.append(key)

        else:
            used_keys.add(element)

            if element not in data:
                missing_keys.append(element)

    additional_keys += [x for x in all_keys if x not in used_keys]

    return missing_keys, additional_keys


if __name__ == '__main__':
    schema = [
        'a',
        'b',
        'c'
    ]
    data = {
        'a': 1,
        'b': 2,
        'c': 3,
        'd': 4
    }

    print(schema_validator(schema, data))
