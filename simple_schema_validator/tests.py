import unittest

from typing import Any

from schema_validator import schema_validator


class SchemaValidatorTests(unittest.TestCase):
    def test_validating_plain_schema(self):
        schema = {
            'a': Any,
            'b': Any,
            'c': Any
        }

        with self.subTest('Test with valid data.'):
            data = {
                'a': 1,
                'b': 2,
                'c': 3
            }

            result = schema_validator(schema, data)

            self.assertEqual(True, bool(result))
            self.assertEqual([], result.missing_keys)
            self.assertEqual([], result.additional_keys)

        with self.subTest('Test with invalid data with missing & additional keys.'):
            data = {
                'a': 1,
                'b': 2,
                'd': 4
            }

            result = schema_validator(schema, data)

            self.assertEqual(False, bool(result))
            self.assertEqual(['c'], result.missing_keys)
            self.assertEqual(['d'], result.additional_keys)

    def test_validating_one_level_nested_schema(self):
        schema = {
            'a': Any,
            'b': Any,
            'c': {
                'd': Any,
                'f': Any
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
            result = schema_validator(schema, data)

            self.assertEqual(True, bool(result))
            self.assertEqual([], result.missing_keys)
            self.assertEqual([], result.additional_keys)

        with self.subTest('Test with invalid data with missing & additional keys.'):
            data = {
                'a': 1,
                'b': 2,
                'c': {
                    'd': 3
                },
                'h': 10
            }

            result = schema_validator(schema, data)

            self.assertEqual(False, bool(result))
            self.assertEqual(['c.f'], result.missing_keys)
            self.assertEqual(['h'], result.additional_keys)

    def test_validating_two_level_nested_schema(self):
        schema = {
            'a': Any,
            'b': Any,
            'c': {
                'd': {
                    'e': Any
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

            result = schema_validator(schema, data)

            self.assertEqual(True, bool(result))
            self.assertEqual([], result.missing_keys)
            self.assertEqual([], result.additional_keys)

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

            result = schema_validator(schema, data)

            self.assertEqual(False, bool(result))
            self.assertEqual(['c.d.e'], result.missing_keys)
            self.assertEqual(['c.d.f'], result.additional_keys)

    def test_validation_multiple_level_nested_schema(self):
        schema = {
            'a': Any,
            'b': Any,
            'c': {
                'd': {
                    'e': {
                        'g': Any,
                        'h': Any
                    }
                }
            },
            'r': Any,
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

            result = schema_validator(schema, data)

            self.assertEqual(True, bool(result))
            self.assertEqual([], result.missing_keys)
            self.assertEqual([], result.additional_keys)

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

            result = schema_validator(schema, data)

            self.assertEqual(False, bool(result))
            self.assertEqual(['c.d.e.g', 'r'], result.missing_keys)
            self.assertEqual(['c.d.e.s', 'c.d.f', 't'], result.additional_keys)


if __name__ == '__main__':
    unittest.main()
