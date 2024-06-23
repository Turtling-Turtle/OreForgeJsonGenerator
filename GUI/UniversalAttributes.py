from typing import Union

from PyQt6.QtWidgets import QWidget, QHBoxLayout

from CLI.Item_Constructors import generate_item_id
from GUI.CustomWidgets.InputField import InputField
from GUI.JsonSerializable import JsonSerializable
from GUI.Validators.StringValidator import StringValidator
from GUI.Validators.Validator import ValidationResult


class UniversalAttributes(QWidget, JsonSerializable):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.itemName = InputField("Name", StringValidator(), "name", valueType=str)
        self.itemName.setLabelToolTip("The name of the item.").setLineEditToolTip("The name of the item.")
        self.layout.addWidget(self.itemName)

        self.itemDescription = InputField("Description", StringValidator(), "description", str)
        self.layout.addWidget(self.itemDescription)

        self.itemID = generate_item_id()
        self.setLayout(self.layout)

    def toDict(self) -> dict:
        results = {}
        results.update(self.itemName.toDict())
        results.update({"id": self.itemID})
        results.update(self.itemDescription.toDict())
        # results.update(self.itemID.toDict())
        return results

    def validate(self) -> Union[ValidationResult, list[ValidationResult]]:
        return [self.itemName.validate(), self.itemDescription.validate()]
