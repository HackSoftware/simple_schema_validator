# Simple schema validator

A dead-simple schema validator, used to validated nested objects for a certain structure. Used in some of our projects.

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
