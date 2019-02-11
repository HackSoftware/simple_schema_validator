import unittest
from schema_validator import schema_validator


class SchemaValidatorTests(unittest.TestCase):
    def test_validating_plain_schema(self):
        schema = {
            'a': None,
            'b': None,
            'c': None
        }


        with self.subTest('Test with valid data.'):
            data = {
                'a': 1,
                'b': 2,
                'c': 3
            }

            value, missing_keys, additional_keys = schema_validator(schema, data)

            self.assertEqual(True, value)
            self.assertEqual([], missing_keys)
            self.assertEqual([], additional_keys)

        with self.subTest('Test with invalid data with missing & additional keys.'):
            data = {
                'a': 1,
                'b': 2,
                'd': 4
            }

            value, missing_keys, additional_keys = schema_validator(schema, data)

            self.assertEqual(False, value)
            self.assertEqual(['c'], missing_keys)
            self.assertEqual(['d'], additional_keys)

    def test_validating_one_level_nested_schema(self):
        schema = {
            'a': None,
            'b': None,
            'c': {
                'd': None,
                'f': None
            }
        }

        with self.subTest('Test with valid data.'):
            data = {
                'a': 1,
                'b': 2,
                'c': {
                    'd': 3,
                    'f': 4
                }
            }
            value, missing_keys, additional_keys = schema_validator(schema, data)

            self.assertEqual(True, value)
            self.assertEqual([], missing_keys)
            self.assertEqual([], additional_keys)

        with self.subTest('Test with invalid data with missing & additional keys.'):
            data = {
                'a': 1,
                'b': 2,
                'c': {
                    'd': 3
                },
                'h': 10
            }

            value, missing_keys, additional_keys = schema_validator(schema, data)

            self.assertEqual(False, value)
            self.assertEqual(['c.f'], missing_keys)
            self.assertEqual(['h'], additional_keys)

    def test_validating_two_level_nested_schema(self):
        schema = {
            'a': None,
            'b': None,
            'c': {
                'd': {
                    'e': None
                }
            }
        }

        with self.subTest('Test with valid data.'):
            data = {
                'a': 1,
                'b': 2,
                'c': {
                    'd': {
                        'e': 3
                    }
                }
            }

            value, missing_keys, additional_keys = schema_validator(schema, data)

            self.assertEqual(True, value)
            self.assertEqual([], missing_keys)
            self.assertEqual([], additional_keys)

        with self.subTest('Test with invalid data with missing & additional keys.'):
            data = {
                'a': 1,
                'b': 2,
                'c': {
                    'd': {
                        'f': 3
                    }
                }
            }

            value, missing_keys, additional_keys = schema_validator(schema, data)

            self.assertEqual(False, value)
            self.assertEqual(['c.d.e'], missing_keys)
            self.assertEqual(['c.d.f'], additional_keys)

    def test_validation_multiple_level_nested_schema(self):
        schema = {
            'a': None,
            'b': None,
            'c': {
                'd': {
                    'e': {
                        'g': None,
                        'h': None
                    }
                }
            },
            'r': None,
        }


        with self.subTest('Test with valid data.'):
            data = {
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

            value, missing_keys, additional_keys = schema_validator(schema, data)

            self.assertEqual(True, value)
            self.assertEqual([], missing_keys)
            self.assertEqual([], additional_keys)

        with self.subTest('Test with invalid data with missing & additional keys.'):
            data = {
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

            value, missing_keys, additional_keys = schema_validator(schema, data)

            self.assertEqual(False, value)
            self.assertEqual(['c.d.e.g', 'r'], missing_keys)
            self.assertEqual(['c.d.e.s', 'c.d.f', 't'], additional_keys)


if __name__ == '__main__':
    unittest.main()
