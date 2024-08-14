from typing import Union

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QCheckBox, QLabel, QHBoxLayout

from GUI.JsonSerializable import JsonSerializable, CustomWidget
from GUI.Validators.StringValidator import StringValidator
from GUI.Validators.Validator import ValidationResult, Validator
from Helper_Functions import bold_string


class OptInWidgetField(QWidget, JsonSerializable, CustomWidget):

    def __init__(self, fieldName: str, keyName: str, customWidget: QWidget):
        QWidget.__init__(self)
        CustomWidget.__init__(self, keyName, "", StringValidator(),)
        self.layout = QHBoxLayout()
        if not isinstance(customWidget, (JsonSerializable, QWidget, CustomWidget)):
            raise TypeError("customWidget must be of type JsonSerializable, is of type" + str(type(customWidget)))

        self.customWidget = customWidget

        self.label = QLabel(bold_string(fieldName))
        self.label.setFont(QFont("Arial", 14))
        self.layout.addWidget(self.label)

        self.checkBox = QCheckBox()
        self.checkBox.stateChanged.connect(self.onCheckBoxToggle)
        self.layout.addWidget(self.checkBox)
        self.layout.addWidget(self.customWidget)
        self.setLayout(self.layout)
        self.onCheckBoxToggle(0)

    """
    TODO: Revisit this at a later date.
    Potential Solution: Change/make sure that game only tries to load the following field if the it was opted into. 
    EX: if canBeSold is true try to get sellPrice otherwise otherwise sellPrice is just set to 0 as a default value cause it cant be sold.
    """

    def toDict(self) -> Union[dict, None]:
        return self.customWidget.toDict() if self.checkBox.isChecked() else None
        # results = {self.keyName: self.checkBox.isChecked()}
        # if self.checkBox.isChecked():
        #     results.update(self.customWidget.toDict())
        #     return results
        # elif self.customWidget.valueType in (int, float):
        #     results.update({self.customWidget.keyName: 0})
        #     return results
        # elif self.customWidget.valueType == str:
        #     results.update({self.customWidget.keyName: ""})
        #     return results
        # raise Exception("CustomWidget Value type must be of type str, int or float. Is of type" + str(
        #     type(self.customWidget.valueType)))

    def validate(self) -> Union[ValidationResult, list[ValidationResult]]:
        return self.customWidget.validate() if self.checkBox.isChecked() else ValidationResult()

    def onCheckBoxToggle(self, state):
        if state == 2:
            self.customWidget.setEnabled(True)
        else:
            self.customWidget.setEnabled(False)

    def setLabelToolTip(self, toolTip: str):
        self.label.setToolTip(toolTip)
        return self

    def setCheckToolTip(self, toolTip: str):
        self.checkBox.setToolTip(toolTip)
        return self
