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
        'type': 'chat',
        'message': [{
            'title': 'Graduation',
            'content': 'Hello there!',
            'urgency': None
        }]
    }

    data_2 = {
        'type': 'data',
        'message': [{
            'title': 'Survey',
            'content': 'N people answered your survey',
            'urgency': 'very urgent'
        }]
    }

    data_3 = {
        'type': 'chat',
        'message': [{
            'title': 'Some titile',
            'content': 'Hello there!',
            'urgency': 1
        }]
    }

    schema = {
        'type': str,
        'message': [{
            'title': str,
            'content': str,
            'urgency': types.Optional[str]
        }]
    }

    print('Validating data_1 ...')
    validate(schema, data_1)

    print('Validating data_2 ...')
    validate(schema, data_2)

    print('Validating data_3 ...')
    validate(schema, data_3)


if __name__ == '__main__':
    main()
