from typing import Union

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QComboBox, QVBoxLayout, QLabel

from GUI.JsonSerializable import JsonSerializable
from GUI.UpgradeStrategyWidgets.StrategyWidget import StrategyWidget
from GUI.Validators.Validator import ValidationResult
from Helper_Functions import bold_string

noe = ("", "")


def ignore(pos):
    pass


class StrategyChoiceField(QWidget, JsonSerializable):

    def __init__(self, choices: dict[str, type(StrategyWidget)], strategyName: str = None):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        if strategyName:
            self.label = QLabel(bold_string(strategyName + ""))
            self.label.setFont(QFont("Arial", 14))
            self.layout.addWidget(self.label)
        self.choices = choices
        self.dropDownMenu = QComboBox(self)
        self.dropDownMenu.wheelEvent = ignore
        for value in self.choices.keys():
            self.dropDownMenu.addItem(value)
        self.dropDownMenu.currentTextChanged.connect(self.updateV2)

        self.layout.addWidget(self.dropDownMenu)
        self.selectedStrategy = choices.get(self.dropDownMenu.currentText())(self)
        self.layout.addWidget(self.selectedStrategy)

    def updateUI(self):
        for key, value in self.choices.items():
            if key == self.dropDownMenu.currentText():
                self.layout.removeWidget(self.selectedStrategy)
                self.selectedStrategy.setParent(None)
                self.selectedStrategy = value(self)
                # self.selectedStrategy.layout.insertWidget(2, self.dropDownMenu)
                for widget in self.selectedStrategy.jsonWidgets:
                    self.layout.addWidget(widget)
                # self.layout.addWidget(self.selectedStrategy)
                self.layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
                return

    def updateV2(self):
        self.selectedStrategy.layout.removeWidget(self.dropDownMenu)
        self.dropDownMenu.setParent(None)
        self.layout.removeWidget(self.selectedStrategy)
        for key, value in self.choices.items():
            if key == self.dropDownMenu.currentText():
                self.selectedStrategy = value(self)
                # self.selectedStrategy.layout.addWidget(self.dropDownMenu)
                self.layout.addWidget(self.selectedStrategy)
                # self.setLayout(self.selectedStrategy)

    def toDict(self) -> dict:
        if isinstance(self.selectedStrategy, JsonSerializable):
            return self.selectedStrategy.toDict()

    def validate(self) -> Union[ValidationResult, list[ValidationResult]]:
        return self.selectedStrategy.validate()
