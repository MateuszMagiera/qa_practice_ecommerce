"""
Utility for validating API/GraphQL responses against JSON Schema contracts.

Usage:
    from utils.schema_validator import assert_valid_schema

    assert_valid_schema(response.json(), "employee_list.json")
"""

import json
import pathlib

import allure
from jsonschema import RefResolver, ValidationError, validate

# Resolve the schemas directory once — works regardless of CWD.
_SCHEMAS_DIR = pathlib.Path(__file__).resolve().parent.parent / "data" / "schemas"


def _load_schema(schema_filename: str) -> dict:
    """Load a JSON Schema file from data/schemas/."""
    schema_path = _SCHEMAS_DIR / schema_filename
    with open(schema_path, encoding="utf-8") as f:
        return json.load(f)


def assert_valid_schema(instance, schema_filename: str) -> None:
    """
    Validate *instance* (a parsed JSON object) against the given schema file.

    - Attaches the schema to the Allure report for traceability.
    - Raises a clear AssertionError (not ValidationError) so pytest shows a nice diff.
    - Supports $ref between schema files in the same directory.
    """
    schema = _load_schema(schema_filename)

    # RefResolver lets schemas reference each other via $ref (e.g. employee_list → employee).
    resolver = RefResolver(
        base_uri=_SCHEMAS_DIR.as_uri() + "/",
        referrer=schema,
    )

    with allure.step(f"Validate response against schema: {schema_filename}"):
        allure.attach(
            json.dumps(schema, indent=2),
            name=f"Schema: {schema_filename}",
            attachment_type=allure.attachment_type.JSON,
        )
        try:
            validate(instance=instance, schema=schema, resolver=resolver)
        except ValidationError as exc:
            allure.attach(
                json.dumps(instance, indent=2, default=str),
                name="Actual response (failed validation)",
                attachment_type=allure.attachment_type.JSON,
            )
            raise AssertionError(
                f"Response does not match schema '{schema_filename}':\n\n"
                f"  Path:    {' → '.join(str(p) for p in exc.absolute_path) or '(root)'}\n"
                f"  Error:   {exc.message}\n"
            ) from None
