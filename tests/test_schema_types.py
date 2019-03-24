from typing import Any

from unittest import TestCase

from simple_schema_validator.schema_types import (
    OptionalTypeFactory,
    is_optional,
    get_optional_type,
    is_optional_schema,
    types
)


class SchemaTypesTests(TestCase):
    def test_optional_type_factory_builds_optional_type(self):
        T = int
        Optional = OptionalTypeFactory()
        v = Optional[T]

        self.assertTrue(is_optional(v))
        self.assertEqual(T, get_optional_type(v))

    def test_is_optional_schema_cases(self):
        optional_schema = types.Optional[{}]

        self.assertTrue(is_optional_schema(optional_schema))

        non_optional_schemas = [
            types.Optional[int],
            types.Optional[float],
            types.Optional[str],
            types.Optional[bool],
            types.Optional[Any],
            types.Optional[[]],
        ]

        for non_optional_schema in non_optional_schemas:
            self.assertFalse(is_optional_schema(non_optional_schema))
