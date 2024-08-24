from typing import Union

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QGridLayout

from CLI.Item_Constructors import generate_item_id
from GUI.CustomWidgets.InputField import InputField
from GUI.JsonSerializable import JsonSerializable
from GUI.Validators.StringValidator import StringValidator
from GUI.Validators.Validator import ValidationResult
from Helper_Functions import bold_string


class UniversalAttributes(QWidget, JsonSerializable):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.itemId = generate_item_id()

        self.itemIdLabel = QLabel(bold_string("ID: ") + self.itemId)
        self.itemIdLabel.setFont(QFont("Arial", 16))
        self.layout.addWidget(self.itemIdLabel)

        self.itemName = InputField("Name", StringValidator(), "name", valueType=str)
        self.itemName.setLabelToolTip("The name of the item.").setLineEditToolTip("The name of the item.")
        self.layout.addWidget(self.itemName, 1, 0, 1, 1)

        self.itemDescription = InputField("Description", StringValidator(), "description", str)
        self.layout.addWidget(self.itemDescription, 1, 1, 1, 1)

        self.setLayout(self.layout)

    def toDict(self) -> dict:
        results = {}
        results.update(self.itemName.toDict())
        results.update({"id": self.itemId})
        results.update(self.itemDescription.toDict())
        # results.update(self.itemID.toDict())
        return results

    def validate(self) -> Union[ValidationResult, list[ValidationResult]]:
        return [self.itemName.validate(), self.itemDescription.validate()]

    def setItemId(self, newID: str) -> None:
        self.itemId = newID
        self.itemIdLabel.setText(bold_string("ID: ") + newID)

    def getItemId(self) -> str:
        return self.itemId