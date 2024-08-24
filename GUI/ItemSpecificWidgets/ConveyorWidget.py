from PyQt6.QtWidgets import QWidget, QVBoxLayout

from GUI.CustomWidgets.InputField import InputField
from GUI.JsonSerializable import JsonSerializable
from GUI.Validators.NumberValidator import NumberValidator


class ConveyorWidget(QWidget, JsonSerializable):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.conveyorSpeed = InputField("Conveyor Speed", NumberValidator(float), "conveyorSpeed", float)
        self.layout.addWidget(self.conveyorSpeed)
        self.setLayout(self.layout)