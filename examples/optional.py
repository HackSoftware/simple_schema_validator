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
        'type': 'data',
        'message': None,
        'data': {
            'foo': 'bar'
        }
    }

    data_2 = {
        'type': 'info',
        'message': 'Some info',
        'data': None
    }

    schema = {
        'type': str,
        'message': types.Optional[str],
        'data': types.Optional[{
            'foo': str
        }]
    }

    print('Validating data_1 ...')
    validate(schema, data_1)

    print('Validating data_2 ...')
    validate(schema, data_2)


if __name__ == '__main__':
    main()
