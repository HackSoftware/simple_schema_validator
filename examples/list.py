from simple_schema_validator import schema_validator, types


def validate(schema, data):
    validation = schema_validator(schema, data)

    if not validation:
        print(f'Keys in data, but not in schema: {validation.additional_keys}')
        print(f'Keys in schema, but not in data: {validation.missing_keys}')
        print(f'Keys with different type from schema {validation.type_errors}')
    else:
        print('Valid.')


def main():
    data_1 = {
        'data': [1, 2, 3]
    }

    data_2 = {
        'data': ['some_string']
    }

    schema = {
        'data': types.List[int]
    }

    print('Validating data_1 ...')
    validate(schema, data_1)

    print('Validating data_2 ...')
    validate(schema, data_2)


if __name__ == '__main__':
    main()
