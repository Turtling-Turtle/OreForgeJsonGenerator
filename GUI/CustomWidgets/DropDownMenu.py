from typing import Union

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QLabel, QComboBox, QHBoxLayout

from GUI.JsonSerializable import JsonSerializable, CustomWidget
from GUI.Validators.Validator import ValidationResult, Validator
from Helper_Functions import bold_string

def ignore(pos):
    pass

class DropDownMenu(QWidget, JsonSerializable, CustomWidget):
    """
    A DropDownMenu takes a list of Tuples.
    [0] is the display name of the element.
    [1] is the valueName of the element.
    """

    def __init__(self, fieldName: str, keyName: str, content: list[tuple[str, str]]):
        QWidget.__init__(self)
        CustomWidget.__init__(self, fieldName, keyName)
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel(bold_string(fieldName))
        self.label.setFont(QFont("Arial", 14))


        self.dropDown = QComboBox()
        self.options = content
        self.dropDown.wheelEvent = ignore
        for element in self.options:
            self.dropDown.addItem(element[0])

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.dropDown)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

    def toDict(self) -> dict:
        for option in self.options:
            if option[0] == self.dropDown.currentText():
                return {self.keyName: option[1]}

    def validate(self) -> Union[ValidationResult, list[ValidationResult]]:
        return ValidationResult()

    def updateContent(self, newOptions: list[tuple[str, str]]):
        self.dropDown.clear()
        self.options = newOptions
        for option in self.options:
            self.dropDown.addItem(option[0])
        self.dropDown.setCurrentText(self.options[0][0])

    def setLabelToolTip(self, toolTip: str):
        self.label.setToolTip(toolTip)
        return self

    def setDropDownToolTip(self, toolTip: str):
        self.dropDown.setToolTip(toolTip)
        return self

    def setBothToolTip(self, toolTip: str):
        self.dropDown.setToolTip(toolTip)
        self.label.setToolTip(toolTip)
        return self
