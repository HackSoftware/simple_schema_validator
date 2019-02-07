import unittest
from schema_validator import schema_validator


class SchemaValidatorTests(unittest.TestCase):
    def test_validating_plain_schema(self):
        schema = [
            'a',
            'b',
            'c'
        ]
        valid_data = {
            'a': 1,
            'b': 2,
            'c': 3
        }
        invalid_data_with_less_keys = {
            'a': 1,
            'b': 2
        }
        invalid_data_with_more_keys = {
            'a': 1,
            'b': 2,
            'c': 3,
            'd': 4
        }
        expected_data_with_less_keys = (False, ['c'], [])
        expected_data_with_more_keys = (False, [], ['d'])

        with self.subTest('Test valid data is valid'):
            self.assertEqual(schema_validator(schema, valid_data), (True, [], []))

        with self.subTest('Test invalid data with less keys'):
            self.assertEqual(schema_validator(schema, invalid_data_with_less_keys), expected_data_with_less_keys)

        with self.subTest('Test invalid data with more keys'):
            self.assertEqual(schema_validator(schema, invalid_data_with_more_keys), expected_data_with_more_keys)

    def test_validating_one_level_nested_schema(self):
        schema = [
            'a',
            'b',
            [
                'c',
                ['d', 'f']
            ]
        ]

        valid_data = {
            'a': 1,
            'b': 2,
            'c': {
                'd': 3,
                'f': 4
            }
        }
        invalid_data_with_less_keys = {
            'a': 1,
            'b': 2,
            'c': {
                'd': 3
            }
        }

        invalid_data_with_more_keys = {
            'a': 1,
            'b': 2,
            'c': {
                'd': 3,
                'f': 4
            },
            'h': 10
        }

        expected_data_with_less_keys = (False, ['c.f'], [])
        expected_data_with_more_keys = (False, [], ['h'])

        with self.subTest('Test valid data is valid'):
            self.assertEqual(schema_validator(schema, valid_data), (True, [], []))

        with self.subTest('Test invalid data with less keys'):
            self.assertEqual(schema_validator(schema, invalid_data_with_less_keys), expected_data_with_less_keys)

        with self.subTest('Test invalid data with more keys'):
            self.assertEqual(schema_validator(schema, invalid_data_with_more_keys), expected_data_with_more_keys)

    def test_validating_two_level_nested_schema(self):
        schema = [
            'a',
            'b',
            [
                'c',
                [
                    [
                        'd', ['e']
                    ]
                ]
            ]
        ]

        valid_data = {
            'a': 1,
            'b': 2,
            'c': {
                'd': {
                    'e': 3
                }
            }
        }
        invalid_data = {
            'a': 1,
            'b': 2,
            'c': {
                'd': {
                    'f': 3
                }
            }
        }

        expected_invalid_data = (False, ['c.d.e'], ['c.d.f'])

        with self.subTest('Test valid data is valid'):
            self.assertEqual(schema_validator(schema, valid_data), (True, [], []))

        with self.subTest('Test invalid data invalid'):
            self.assertEqual(schema_validator(schema, invalid_data), expected_invalid_data)

    def test_validation_multiple_level_nested_schema(self):
        schema = [
            'a',
            'b',
            [
                'c',
                [
                    [
                        'd',
                        [
                            [
                                'e', ['g', 'h']
                            ]
                        ]
                    ]
                ]
            ],
            'r'
        ]

        valid_data = {
            'a': 1,
            'b': 2,
            'c': {
                'd': {
                    'e': {
                        'g': 2,
                        'h': 3
                    }
                }
            },
            'r': 23,
        }
        invalid_data = {
            'a': 1,
            'b': 2,
            'c': {
                'd': {
                    'f': 12,
                    'e': {
                        'h': 3,
                        's': 2
                    }
                }
            },
            't': 2
        }

        expected_invalid_data = (False, ['c.d.e.g', 'r'], ['c.d.e.s', 'c.d.f',  't'])

        with self.subTest('Test valid data is valid'):
            self.assertEqual(schema_validator(schema, valid_data), (True, [], []))

        with self.subTest('Test invalid data invalid'):
            self.assertEqual(schema_validator(schema, invalid_data), expected_invalid_data)


if __name__ == '__main__':
    unittest.main()
