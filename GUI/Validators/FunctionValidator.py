from GUI.JsonSerializable import JsonSerializable
from GUI.Validators.ExpressionValidators import validate_function
from GUI.Validators.Validator import Validator, ValidationResult
from GUI.Widgets import InputField


class FunctionValidator(Validator):
    def __init__(self, parent: InputField):
        super().__init__()
        self.parent = parent

    def validate(self, inputData) -> ValidationResult:
        if len(inputData) <= 0:
            return ValidationResult(self.parent + "Field is empty")
        result = validate_function(inputData)
        if isinstance(result, str):
            return ValidationResult(result)
        else:
            self.parent.lineEdit.setText(result.get_nowait())
            return ValidationResult()
