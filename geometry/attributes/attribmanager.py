import json
import jsonschema
from jsonschema import validate


class AttribManager:

    def __init__(self):
        self.prototypes = []
        self.attributes = []

        with open("geometry/attributes/attribprototype.json", 'r') as file:
            input = json.load(file)

        with open("geometry/attributes/attrib_schema.json", 'r') as file:
            schemas = json.load(file)

        self.prototypes = input['prototypes']

        invalid_prototypes = []
        # valid attribute prototypes
        for prototype in self.prototypes:
            check = self.validate_attribute(prototype, schemas)
            if not check:
                invalid_prototypes.append(prototype)

        # remove invalid attribute prototypes
        for att in invalid_prototypes:
            self.prototypes.remove(att)

    def getPrototypes(self):
        return self.prototypes

    def getAttributes(self):
        return self.attributes

    def getAttributeByName(self, _name):
        for attribute in self.attributes:
            if attribute['name'] == _name:
                return attribute

    def removeAttribute(self, _attribute):
        self.attributes.remove(_attribute)

    def getPrototypeByType(self, _type):
        for prototype in self.prototypes:
            if prototype['type'] == _type:
                return prototype

    def createAttributeFromPrototype(self, _type, _name):

        # checks if an attribute with that name already exists
        for atributte in self.attributes:
            if atributte['name'] == _name:
                return False

        # get the prototype to create the name of the new attribute
        for prototype in self.prototypes:
            if prototype['type'] == _type:
                prototype_target = prototype.copy()
                prototype_target['properties'] = prototype['properties'].copy()
                self.attributes.append(prototype_target)
                prototype_target['name'] = _name
                return True

    def setAttributeValues(self, _name, _values):
        attribute = self.getAttributeByName(_name)
        attValues = attribute['properties']

        index = 0
        for key in attValues:
            attValues[key] = _values[index]
            index += 1

    def validate_attribute(self, _attribute, _schemas):

        for prototype in self.prototypes:
            if _attribute['type'] == prototype['type']:
                if _attribute != prototype:
                    print(
                        f"There cannot be two prototypes of the same type: {_attribute['type']}")
                    return False

        check = AttribManager.validate_schema(
            _attribute, _schemas['att_schema'])
        if not check:
            return False

        values_types = []
        properties = _attribute['properties']
        for key in properties:
            valueType = type(properties[key])
            if valueType == int:
                values_types.append("int")
            elif valueType == float:
                values_types.append("float")
            elif valueType == bool:
                values_types.append("bool")
            elif valueType == str:
                values_types.append("string")
            elif valueType == list:
                values_types.append("color")
                color_dict = properties[key]
                check = AttribManager.validate_schema(
                    color_dict, _schemas['color_schema'])
                if not check:
                    return False
            elif valueType == dict:
                values_types.append("options")
                options_dict = properties[key]
                check = AttribManager.validate_schema(
                    options_dict, _schemas['options_schema'])
                if not check:
                    return False

                if options_dict['index'] < 0 or options_dict['index'] > (len(options_dict['list'])-1):
                    print("Given Attribute is InValid: index out of range")
                    print(_attribute)
                    return False

        # creates a new key
        _attribute['properties_type'] = values_types.copy()

        return True

    @staticmethod
    def validate_schema(_objetc, _schema):
        try:
            validate(instance=_objetc, schema=_schema)
            return True
        except jsonschema.exceptions.ValidationError as err:
            print("Given Attribute is InValid")
            print(_objetc)
            print(err)
            return False
