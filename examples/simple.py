from simple_schema_validator import schema_validator


def main():
    data = {
        'status': 'OK',
        'data': {
            'id': 1,
            'email': 'radorado@hacksoft.io',
            'age': '29',
            'username': 'radorado'
        }
    }

    schema = {
        'status': str,
        'data': {
            'id': int,
            'email': str,
            'age': int,
            'token': str
        }
    }

    validation = schema_validator(schema, data)

    if not validation:
        print(f'Keys in data, but not in schema: {validation.additional_keys}')
        print(f'Keys in schema, but not in data: {validation.missing_keys}')
        print(f'Keys with different type from schema {validation.type_errors}')


if __name__ == '__main__':
    main()
