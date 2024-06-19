from abc import ABC, abstractmethod
from typing import Union

from GUI.Validators.Validator import ValidationResult, Validator


class JsonSerializable(ABC):
    def __init__(self, fieldName: str, validator: Validator, keyName: str, valueType: type = None):
        # if valueType not in (str, int, float, bool):
        #     raise ValueError(f'Value type {valueType} is not valid')
        self.valueType = valueType
        self.keyName = keyName
        self.fieldName = fieldName
        self.validator = validator
        self.validator.setParentFieldName(fieldName)

    @abstractmethod
    def toDict(self) -> dict:
        pass

    @abstractmethod
    def validate(self) -> Union[ValidationResult, list[ValidationResult]]:
        pass

