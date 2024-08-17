import abc
from typing import Union

from GUI.Validators.Validator import ValidationResult, Validator


class JsonSerializable:
    @abc.abstractmethod
    def toDict(self) -> dict:
        data = {}
        for field in vars(self).values():
            if isinstance(field, JsonSerializable):
                data.update(field.toDict())
        return data

    @abc.abstractmethod
    def validate(self) -> Union[ValidationResult, list[ValidationResult]]:
        results = []
        for field in vars(self).items():
            if isinstance(field, JsonSerializable):
                result = field.validate()
                results.extend(result) if isinstance(result, list) else results.append(result)
        return results


class CustomWidget:
    def __init__(self, fieldName: str, keyName: str, validator: Validator = None, valueType: type = None):
        # if valueType not in (str, int, float, bool):
        #     raise ValueError(f'Value type {valueType} is not valid')
        self.valueType = valueType
        self.keyName = keyName
        self.fieldName = fieldName
        self.validator = validator
        if self.validator:
            self.validator.setParentFieldName(fieldName)
