import unittest

from typing import Any

from schema_validator import schema_validator, types


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

    def test_validating_multiple_level_nested_schema(self):
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

    def test_validating_types_with_plain_schema(self):
        with self.subTest('Valid schema, invalid types'):
            schema = {
                'a': int,
            }

            data = {
                'a': 'some_string'
            }

            result = schema_validator(schema, data)

            self.assertEqual(False, bool(result))
            self.assertEqual([], result.missing_keys)
            self.assertEqual([], result.additional_keys)
            self.assertEqual(
                [{'path': 'a', 'expected': int, 'actual': str}],
                result.type_errors
            )

        with self.subTest('Valid schema, valid types'):
            schema = {
                'a': int,
            }

            data = {
                'a': 1
            }

            result = schema_validator(schema, data)

            self.assertEqual(True, bool(result))
            self.assertEqual([], result.missing_keys)
            self.assertEqual([], result.additional_keys)

        with self.subTest('Invalid schema, invalid types'):
            schema = {
                'a': int,
                'b': str
            }

            data = {
                'a': 'some_string',
                'c': 1
            }

            result = schema_validator(schema, data)

            self.assertEqual(False, bool(result))
            self.assertEqual(['b'], result.missing_keys)
            self.assertEqual(['c'], result.additional_keys)
            self.assertEqual(
                [{'path': 'a', 'expected': int, 'actual': str}],
                result.type_errors
            )

        with self.subTest('Invalid schema, valid types'):
            schema = {
                'a': int,
                'b': str
            }

            data = {
                'a': 1,
                'c': 1
            }

            result = schema_validator(schema, data)

            self.assertEqual(False, bool(result))
            self.assertEqual(['b'], result.missing_keys)
            self.assertEqual(['c'], result.additional_keys)
            self.assertEqual([], result.type_errors)

    def test_validating_different_types(self):
        with self.subTest('Valid types'):
            schema = {
                'a': int,
                'b': str,
                'c': float,
                'd': bool,
                'e': None
            }

            data = {
                'a': 1,
                'b': 'some_string',
                'c': 1.0,
                'd': True,
                'e': None
            }

            result = schema_validator(schema, data)

            self.assertEqual(True, bool(result))
            self.assertEqual([], result.missing_keys)
            self.assertEqual([], result.additional_keys)
            self.assertEqual([], result.type_errors)

        with self.subTest('Invalid types'):
            schema = {
                'a': int,
                'b': str,
                'c': float,
                'd': bool,
                'e': None
            }

            data = {
                'a': 'some_string',
                'b': 1.0,
                'c': 1,
                'd': None,
                'e': 'some_string'
            }

            result = schema_validator(schema, data)

            self.assertEqual(False, bool(result))
            self.assertEqual([], result.missing_keys)
            self.assertEqual([], result.additional_keys)
            self.assertEqual(
                [
                    {'actual': str, 'expected': int, 'path': 'a'},
                    {'actual': float, 'expected': str, 'path': 'b'},
                    {'actual': int, 'expected': float, 'path': 'c'},
                    {'actual': None, 'expected': bool, 'path': 'd'},
                    {'actual': str, 'expected': None, 'path': 'e'}
                ],
                result.type_errors
            )

    def test_validating_types_with_nested_schema(self):
        with self.subTest('Valid schema, invalid types'):
            schema = {
                'a': int,
                'b': int,
                'c': {
                    'd': {
                        'e': int
                    }
                }
            }

            data = {
                'a': 'some_string',
                'b': 'some_string',
                'c': {
                    'd': {
                        'e': 'some_string'
                    }
                }
            }

            result = schema_validator(schema, data)

            self.assertEqual(False, bool(result))
            self.assertEqual([], result.missing_keys)
            self.assertEqual([], result.additional_keys)
            self.assertEqual(
                [
                    {'path': 'a', 'expected': int, 'actual': str},
                    {'path': 'b', 'expected': int, 'actual': str},
                    {'path': 'c.d.e', 'expected': int, 'actual': str}
                ],
                result.type_errors
            )

        with self.subTest('Valid schema, valid types'):
            schema = {
                'a': int,
                'b': int,
                'c': {
                    'd': {
                        'e': int
                    }
                }
            }

            data = {
                'a': 1,
                'b': 1,
                'c': {
                    'd': {
                        'e': 1
                    }
                }
            }

            result = schema_validator(schema, data)

            self.assertEqual(True, bool(result))
            self.assertEqual([], result.missing_keys)
            self.assertEqual([], result.additional_keys)
            self.assertEqual([], result.type_errors)

        with self.subTest('Invalid schema, invalid types'):
            schema = {
                'a': int,
                'b': int,
                'c': {
                    'd': {
                        'e': int
                    }
                }
            }

            data = {
                'a': 'some_string',
                'c': {
                    'd': {
                        'e': 'some_string',
                        'g': 2
                    }
                },
                'f': 1
            }

            result = schema_validator(schema, data)

            self.assertEqual(False, bool(result))
            self.assertEqual(['b'], result.missing_keys)
            self.assertEqual(['c.d.g', 'f'], result.additional_keys)
            self.assertEqual(
                [
                    {'path': 'a', 'expected': int, 'actual': str},
                    {'path': 'c.d.e', 'expected': int, 'actual': str},
                ],
                result.type_errors
            )

        with self.subTest('Invalid schema, valid types'):
            schema = {
                'a': int,
                'b': int,
                'c': {
                    'd': {
                        'e': int
                    }
                }
            }

            data = {
                'a': 1,
                'c': {
                    'd': {
                        'e': 1,
                        'g': 2
                    }
                },
                'f': 1
            }

            result = schema_validator(schema, data)

            self.assertEqual(False, bool(result))
            self.assertEqual(['b'], result.missing_keys)
            self.assertEqual(['c.d.g', 'f'], result.additional_keys)
            self.assertEqual([], result.type_errors)

    def test_validating_optional_type(self):
        schema = {
            'a': types.Optional[int]
        }

        with self.subTest('None is valid for optional'):
            data = {
                'a': None
            }

            result = schema_validator(schema, data)

            self.assertEqual(True, bool(result))
            self.assertEqual([], result.missing_keys)
            self.assertEqual([], result.additional_keys)
            self.assertEqual([], result.type_errors)

        with self.subTest('T is valid for Optional[T]'):
            data = {
                'a': 1
            }

            result = schema_validator(schema, data)

            self.assertEqual(True, bool(result))
            self.assertEqual([], result.missing_keys)
            self.assertEqual([], result.additional_keys)
            self.assertEqual([], result.type_errors)

        with self.subTest('X is invalid for Optional[T]'):
            data = {
                'a': 'some_string'
            }

            result = schema_validator(schema, data)

            self.assertEqual(False, bool(result))
            self.assertEqual([], result.missing_keys)
            self.assertEqual([], result.additional_keys)
            self.assertEqual(
                [{'path': 'a', 'expected': int, 'actual': str}],
                result.type_errors
            )

    def test_validating_optional_schema(self):
        schema = {
            'foo': types.Optional[{
                'bar': int,
                'baz': {
                    'a': int,
                    'b': int,
                    'c': int
                }
            }]
        }

        with self.subTest('None is valid for Optional[Schema]'):
            data = {
                'foo': None
            }

            result = schema_validator(schema, data)

            self.assertEqual(True, bool(result))
            self.assertEqual([], result.missing_keys)
            self.assertEqual([], result.additional_keys)
            self.assertEqual([], result.type_errors)

        with self.subTest('Schema is valid for Optional[Schema]'):
            data = {
                'foo': {
                    'bar': 1,
                    'baz': {
                        'a': 1,
                        'b': 1,
                        'c': 1
                    }
                }
            }

            result = schema_validator(schema, data)

            self.assertEqual(True, bool(result))
            self.assertEqual([], result.missing_keys)
            self.assertEqual([], result.additional_keys)
            self.assertEqual([], result.type_errors)

    def test_validating_deeply_nested_optional_schema(self):
        schema = {
            'a': types.Optional[{
                'b': types.Optional[{
                    'c': int
                }]
            }]
        }

        with self.subTest('Value of key `a` can be None'):
            data = {
                'a': None
            }

            result = schema_validator(schema, data)

            self.assertEqual(True, bool(result))
            self.assertEqual([], result.missing_keys)
            self.assertEqual([], result.additional_keys)
            self.assertEqual([], result.type_errors)

        with self.subTest('Value of key `a.b` can be None'):
            data = {
                'a': {
                    'b': None
                }
            }

            result = schema_validator(schema, data)

            self.assertEqual(True, bool(result))
            self.assertEqual([], result.missing_keys)
            self.assertEqual([], result.additional_keys)
            self.assertEqual([], result.type_errors)

        with self.subTest('Value of key `a.b` can be invalid'):
            data = {
                'a': {
                    'b': 1
                }
            }

            result = schema_validator(schema, data)

            self.assertEqual(False, bool(result))
            self.assertEqual(['a.b.c'], result.missing_keys)
            self.assertEqual([], result.additional_keys)
            self.assertEqual(
                [
                    {
                        'path': 'a.b',
                        'expected': {'c': int},
                        'actual': int
                    }
                ],
                result.type_errors
            )

        with self.subTest('Value of key `a.b.c` can be valid'):
            data = {
                'a': {
                    'b': {
                        'c': 1
                    }
                }
            }

            result = schema_validator(schema, data)

            self.assertEqual(True, bool(result))
            self.assertEqual([], result.missing_keys)
            self.assertEqual([], result.additional_keys)
            self.assertEqual([], result.type_errors)

        with self.subTest('Value of key `a.b.c` can be invalid'):
            data = {
                'a': {
                    'b': {
                        'c': 'some_string'
                    }
                }
            }

            result = schema_validator(schema, data)

            self.assertEqual(False, bool(result))
            self.assertEqual([], result.missing_keys)
            self.assertEqual([], result.additional_keys)
            self.assertEqual(
                [{'path': 'a.b.c', 'expected': int, 'actual': str}],
                result.type_errors
            )


if __name__ == '__main__':
    unittest.main()
