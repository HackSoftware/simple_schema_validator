from unittest import TestCase

from simple_schema_validator.utils import get_paths, set_nested


class UtilsTests(TestCase):
    def test_get_paths(self):
        data = {
            'a': 1,
            'b': {
                'c': 2,
                'd': {
                    'f': 3
                }
            }
        }

        paths = get_paths(data)

        self.assertEqual(
            {
                'a': 1,
                'b': {
                    'c': 2,
                    'd': {
                        'f': 3
                    }
                },
                'b.c': 2,
                'b.d': {
                    'f': 3
                },
                'b.d.f': 3
            },
            paths
        )

    def test_set_nested(self):
        value = 'foo'

        data = {
            'a': 1,
            'b': {
                'c': 2,
                'd': {
                    'f': 3
                }
            }
        }

        with self.subTest('Setting on first level works'):
            set_nested(data, 'a', value)

            self.assertEqual(data['a'], value)

        with self.subTest('Setting nested works'):
            set_nested(data, 'b.d.f', value)

            self.assertEqual(data['b']['d']['f'], value)
