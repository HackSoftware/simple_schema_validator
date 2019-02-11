# Simple schema validator

A dead-simple utility that validates if object has a certain structure. Used in some of our projects.

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
  'user': None,
  'profile': {
    'email': None,
    'name': None,
    'age': None
  },
  'tokens': {
    'jwt': None,
    'refresh': None,
    'firebase': None
  }
}

valid, missing_keys, additional_keys = schema_validator(schema, data)

assert valid, f'Response not valid, missing: {missing_keys}, additional: {additional_keys}'
```

* `missing_keys` are those keys that are required in the `schema`, but not found in `data`.
* `additional_keys` are those keys present in `data`, but not required by the `schema`.
* Nested keys are represented with "dot" notation - `profile.email`, `tokens.jwt`, etc.
