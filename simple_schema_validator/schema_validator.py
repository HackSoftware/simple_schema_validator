from copy import deepcopy

from typing import List, Dict, Any, Optional

from operator import itemgetter

from .schema_types import type_check
from .utils import replace_optional_schema_paths, get_paths, get_paths_with_any


MissingKeys = List[str]
AdditionalKeys = List[str]
Schema = Dict[str, Any]
Data = Dict[str, Any]

Paths = Dict[str, Optional[str]]  # item: parent
OptionalPaths = List[str]


class SchemaValidationResult:
    def __init__(self, *, valid, missing_keys, additional_keys, type_errors):
        self.__valid = valid
        self.__missing_keys = missing_keys
        self.__additional_keys = additional_keys
        self.__type_errors = type_errors

    @property
    def missing_keys(self):
        return self.__missing_keys

    @property
    def additional_keys(self):
        return self.__additional_keys

    @property
    def type_errors(self):
        return self.__type_errors

    def __bool__(self):
        return self.__valid


def remove_optional_values(data_paths_mapping, optional_paths, schema_paths):
    paths_to_remove = set()

    for optional_path in optional_paths:
        value = data_paths_mapping.get(optional_path, None)

        if value is None:
            for schema_path in schema_paths:
                if schema_path != optional_path and schema_path.startswith(optional_path):
                    paths_to_remove.add(schema_path)

    return schema_paths - paths_to_remove


def remove_paths_inside_paths_of_any(data_paths, schema_paths_mapping):
    paths_with_any = get_paths_with_any(schema_paths_mapping)

    paths_to_remove = set()

    for path in data_paths:
        for path_with_any in paths_with_any:
            if path.startswith(path_with_any) and path != path_with_any:
                paths_to_remove.add(path)

    return data_paths - paths_to_remove


def schema_validator(schema: Schema, data: Data) -> SchemaValidationResult:
    schema = deepcopy(schema)

    schema_paths_mapping, optional_paths = replace_optional_schema_paths(schema)
    data_paths_mapping = get_paths(data)

    schema_paths = set(schema_paths_mapping)
    data_paths = set(data_paths_mapping)

    optional_paths = set(optional_paths)

    schema_paths = remove_optional_values(data_paths_mapping, optional_paths, schema_paths)
    data_paths = remove_paths_inside_paths_of_any(data_paths, schema_paths_mapping)

    missing_keys = schema_paths - data_paths
    additional_keys = data_paths - schema_paths

    existing_paths_in_schema = data_paths - additional_keys
    type_errors = []

    for path in existing_paths_in_schema:
        valid_type, type_error = type_check(
            schema_paths_mapping,
            data_paths_mapping,
            path,
            optional_paths
        )

        if not valid_type:
            type_errors.append(type_error)

    return SchemaValidationResult(
        valid=schema_paths == data_paths and not type_errors,
        missing_keys=sorted(missing_keys),
        additional_keys=sorted(additional_keys),
        type_errors=sorted(type_errors, key=itemgetter('path'))
    )
