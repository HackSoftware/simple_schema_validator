# Simple schema validator

- [Simple schema validator](#simple-schema-validator)
    - [Basic usage](#basic-usage)
    - [Type checking](#type-checking)
        - [Optional types](#optional-types)


A dead-simple utility that validates if object has a certain structure. Used in some of our projects.

## Basic usage

```
pip install simple_schema_validator
```

An example:

Lets say we have an API that returns the following data:

```json
{
  "user": 1,
  "profile": {
    "email": "some@user.com",
    "name": "Some User",
    "age": 20
  },
  "tokens": {
    "jwt": "...",
    "refresh": "...",
    "firebase": "...",
  }
}
```

And we are writing a simple integration test, that wants to assure the response has a certain structure.

Then we can use the schema validator like so:

```python
from simple_schema_validator import schema_validator

data = get_data_from_api()

schema = {
  'user': Any,
  'profile': {
    'email': Any,
    'name': Any,
    'age': Any
  },
  'tokens': {
    'jwt': Any,
    'refresh': Any,
    'firebase': Any
  }
}

validation = schema_validator(schema, data)

if not result:
    print(f'Keys in data, but not in schema: {validation.additional_keys}')
    print(f'Keys in schema, but not in data: {validation.missing_keys}')
    print(f'Keys with different type from schema {validation.type_errors}')
```

* `missing_keys` are those keys that are required in the `schema`, but not found in `data`.
* `additional_keys` are those keys present in `data`, but not required by the `schema`.
* `validation_errors` are those keys, that are having a different type in `data`, from the defined in `schema`.

**Nested keys are represented with "dot" notation - `profile.email`, `tokens.jwt`, etc.**

## Type checking

The util supports simple schema type checking.

Currently, the supported types in the schema are:

* `int`
* `float`
* `str`
* `bool`
* `typing.Any` (from Python `typing` library)
* `simple_schema_validator.types.Optional` (custom type, define in the package)

If the type is `Any`, no type checking is done.

If there's a type mismatch, the errors are placed in the `type_errors` attribute of the result, which is a list of type errors.

The general format of a single type error is:

```python
{
  'path': 'the.path.to.the.value.in.data',
  'expected': the_expected_type_as_defined_in_the_schema,
  'actual': the_actual_type_of_the_value
}
```

Here's an example:


```python
from simple_schema_validator import schema_validator, types


schema = {
  'user': str,
  'profile': {
    'email': str,
    'name': str,
    'age': int
  },
  'tokens': {
    'jwt': str,
    'refresh': str,
    'firebase': str
  }
}

data = {
  'user': 'Some User',
  'profile': {
    'email': 'someuser@hacksoft.io',
    'name': 'Some User',
    'age': "29"
  },
  'tokens': {
    'jwt': 'some token value',
    'refresh': 'some token value',
    'firebase': 'some token value'
  }

}

result = schema_validator(schema, data)


assert bool(result) is False
assert result.type_errors == [{'path': 'profile.age', 'expected': int, 'actual': str}]
```

### Optional types

The schema validator support optional types.

You can do the following:

```python
from simple_schema_validator import schema_validator, types

schema = {
  'a': types.Optional[int]
}

data_1 = {
  'a': None
}

data_2 = {
  'a': 1
}

data_3 = {
  'a': 'some_string'
}

assert bool(schema_validator(schema, data_1)) is True
assert bool(schema_validator(schema, data_2)) is True
assert bool(schema_validator(schema, data_3)) is False
```

Additionally, you can define optional branches in the schema:

```python
from simple_schema_validator import schema_validator, types

schema = {
  'a': types.Optional[{
    'b': int
  }]
}

data_1 = {
  'a': None
}

data_2 = {
  'a': 1
}

data_3 = {
  'a': {
    'b': 1
  }
}

data_4 = {
  'a': {
    'b': 'some_string'
  }
}

assert bool(schema_validator(schema, data_1)) is True
assert bool(schema_validator(schema, data_2)) is False
assert bool(schema_validator(schema, data_3)) is True
assert bool(schema_validator(schema, data_4)) is False
```

## Examples

For examples, check the [examples](examples/) folder or the tests for the project.
