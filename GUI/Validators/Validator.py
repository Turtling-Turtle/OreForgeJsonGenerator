from abc import ABC, abstractmethod


class ValidationResult:
    """
    """

    def __init__(self, errorMessage: str = None):
        self.hasError = errorMessage is not None
        self.errorMessage = errorMessage

    def isError(self) -> bool:
        return self.hasError

    def errorMessage(self) -> str:
        return self.errorMessage


class Validator(ABC):
    def __init__(self):
        self.fieldName = ""

    @abstractmethod
    def validate(self, inputData) -> ValidationResult:
        pass

    def setParentFieldName(self, parentFieldName: str):
        self.fieldName = parentFieldName
