from GUI.Validators.Validator import Validator, ValidationResult


class ConditionValidator(Validator):
    def __init__(self):
        super().__init__()

    def validate(self, inputData) -> ValidationResult:
        print("Warning Condition Validator Method has not been implemented yet!")
        return ValidationResult()
