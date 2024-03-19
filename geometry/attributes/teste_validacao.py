import json
import jsonschema
from jsonschema import validate

with open("geometry/attributes/attributes.json", 'r') as file:
    input = json.load(file)

with open("geometry/attributes/schema.json", 'r') as file:
    schema = json.load(file)

attClasses = input['classes']


def validate_schema(_objetc, _schema):
    try:
        validate(instance=_objetc, schema=_schema)
        print("Given Attribute is Valid")
    except jsonschema.exceptions.ValidationError as err:
        print("Given Attribute is InValid")
        print(_objetc)
        print(err)


for attClasse in attClasses:
    validate_schema(attClasse, schema)
