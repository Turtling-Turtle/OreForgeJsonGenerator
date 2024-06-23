from GUI.Validators.Validator import Validator, ValidationResult


def isFloat(value: str):
    try:
        float(value)
        return True
    except ValueError:
        return False


def isInteger(value: str):
    try:
        int(value)
        return True
    except ValueError:
        return False


class NumberValidator(Validator):
    """
    A NumberValidator takes an input string and checks if it is a number.
    It can compare it against a minimum and maximum value.

    """

    def __init__(self, numberType: type, min_value=None, max_value=None):
        super().__init__()
        # self.setParentFieldName(parentFieldName)
        if numberType not in (float, int):
            raise TypeError("Unsupported type for input data: " + str(numberType) + ", expected float or int.")
        self.numberType = numberType
        self.minimumValue = min_value
        self.maximumValue = max_value

    def validate(self, inputData) -> ValidationResult:
        if self.numberType == float:
            if isFloat(inputData):
                return self.compareRange(float(inputData))
            else:
                return ValidationResult(
                    "Inputted value in " + self.fieldName + " field is not a valid floating point number.")

        if self.numberType == int:
            if isInteger(inputData):
                return self.compareRange(int(inputData))
            else:
                return ValidationResult("Inputted value in " + self.fieldName + " field is not a valid integer.")
        raise TypeError("Unsupported type for input data: " + self.numberType.__str__() + ", expected float or int.")

    def compareRange(self, inputValue) -> ValidationResult:
        if self.minimumValue is not None and inputValue < self.minimumValue:
            return ValidationResult(
                "Inputted Value in " + self.fieldName + " field is less than the minimum value of" +
                str(self.minimumValue))
        if self.maximumValue is not None and inputValue > self.maximumValue:
            return ValidationResult(
                "Inputted Value in " + self.fieldName + " field is greater than the max value of " +
                str(self.maximumValue))
        return ValidationResult()
