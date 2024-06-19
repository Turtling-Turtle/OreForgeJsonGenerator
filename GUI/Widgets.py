from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QComboBox, QCheckBox

from Helper_Functions import is_numeric


class JsonSerializable:

    def toJson(self):
        raise NotImplemented()

    """
    Verifies that the current data is valid Json for OreForge.
    returns None if the data is valid
    :returns str  if the data is invalid
    :returns list[str] if the widget has multiple fields data is invalid
    """

    def isValid(self):
        raise NotImplemented()


class InputField(QWidget, JsonSerializable):
    # TODO: Make it so input field filters out invalid characters(Ex: field that only takes numbers)
    """
    An input field Consists of a Label and a LineEdit.
    You can specify the accepted input for the field EX: field that only accepts floats etc.
    """

    def __init__(self, LabelName: str, fontSize=14, isInteger: bool = False, isFloat: bool = False,
                 label_tip: str = None, edit_tip=None, maxValue: float = None, minValue: float = None):
        super().__init__()
        self.maxValue = maxValue
        self.minValue = minValue
        self.name = LabelName
        self.hbox = QHBoxLayout()
        self.isInteger = isInteger
        self.isFloat = isFloat
        self.label = QLabel(bold_string(LabelName))
        self.label.setToolTip(label_tip)
        self.label.setFont(QFont("Arial", fontSize))
        self.lineEdit = QLineEdit()
        self.lineEdit.setToolTip(label_tip)
        self.hbox.addWidget(self.label)
        self.hbox.addWidget(self.lineEdit)
        self.hbox.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.setLayout(self.hbox)

    def getFieldData(self):
        if self.isInteger:
            return int(self.lineEdit.text())
        elif self.isFloat:
            return float(self.lineEdit.text())
        return self.lineEdit.text()

    def clear(self):
        self.lineEdit.setText("")

    def setEnabled(self, enabled):
        self.label.setEnabled(enabled)
        self.lineEdit.setEnabled(enabled)

    def toJson(self):
        return self.getFieldData()

    def isValid(self):
        if len(self.lineEdit.text()) <= 0:
            return "*" + self.name + " is empty"
        elif self.isInteger:
            try:
                value = int(self.lineEdit.text())
                if self.maxValue is not None and value > self.maxValue:
                    return "*" + self.name + " exceeds the max value of " + str(self.maxValue)
                if self.minValue is not None and value < self.minValue:
                    return "*" + self.name + " is less than the min value of " + str(self.minValue)
                return None
            except ValueError:
                return "* Input in " + self.name + " field is not an integer"
        elif self.isFloat:
            try:
                value = float(self.lineEdit.text())
                if self.maxValue is not None and value > self.maxValue:
                    return "*" + self.name + " exceeds the max value of " + str(self.maxValue)
                if self.maxValue is not None and value < self.minValue:
                    return "*" + self.name + " is less than the min value of " + str(self.minValue)
                return None
            except ValueError:
                return "* Input in " + self.name + " field is not a valid float"

    def __str__(self):
        return self.label.text()

    def set_label_tip(self, text):
        self.label.setToolTip(text)

    def set_edit_tip(self, text):
        self.lineEdit.setToolTip(text)

    def set_both_tips(self, text):
        self.set_label_tip(text)
        self.set_edit_tip(text)


class DropDownMenu(QWidget, JsonSerializable):
    # element[0] is display name, element[1] is real/true name.
    """
    A DropDown Menu Takes a list of tuples.
    [0] is the Display name of the content
    [1] is the Json name of the content.
    """

    def __init__(self, content: list[tuple[str, str]], label_name: str, label_tip: str = None, box_tip: str = None):
        super().__init__()
        self.label = QLabel(bold_string(label_name))
        self.label.setFont(QFont("Arial", 14))
        self.label.setToolTip(label_tip)
        self.comboBox = QComboBox()
        self.comboBox.setToolTip(box_tip)
        self.content = content
        for element in content:
            self.comboBox.addItem(element[0])
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.label)
        self.hbox.addWidget(self.comboBox)
        self.hbox.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.setLayout(self.hbox)

    def clear(self):
        pass

    def setEnabled(self, enabled):
        self.label.setEnabled(enabled)
        self.comboBox.setEnabled(enabled)

    def toJson(self):
        for element in self.content:
            if element[0] == self.comboBox.currentText():
                return element[1]
        return None

    def isValid(self):
        return None

    def __str__(self):
        return self.label.text()


class OptInField(QWidget, JsonSerializable):
    """
    An optional field takes another QWidget that "implements" JsonSerializable.

    When using an OptionalField you must specify the behavior of to_json and isValid methods.
    This can be done using lamda expressions and the setIsvalid and set_to_json methods.

    booleanJsonKey and widgetJsonKey are used the keys for the fields that this widget returns

    Normally looks like this:
    to_json_behavior = Lambda self: {
        self.widgetJsonKey : self.customWidget.to_json() if self.checkBox.isChecked() else None
    }
    object.set_to_json(lambda: to_json_behavior(self.object))

    alternatively you could do something like this instead:
    to_json_behavior = Lambda self: {
        "yourFieldName": self.customWidget.to_json() if self.checkBox.isChecked() else None
    }
    """

    def __init__(self, customWidget: JsonSerializable, checkBoxPrompt: str, booleanJsonKey: str = None,
                 widgetJsonKey: str = None):
        super().__init__()
        self.booleanJsonKey = booleanJsonKey
        self.widgetJsonKey = widgetJsonKey
        self.checkBox = QCheckBox(checkBoxPrompt)
        self.customWidget = customWidget
        self.checkBox.stateChanged.connect(self.onCheckBoxToggle)
        self.layout = QHBoxLayout()

        self.layout.addWidget(self.checkBox)
        self.layout.addWidget(self.customWidget)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        self.setLayout(self.layout)
        self.onCheckBoxToggle(self.checkBox.stateChanged)

    def onCheckBoxToggle(self, state):
        if state == 2:
            self.customWidget.setEnabled(True)
        else:
            self.customWidget.clear()
            self.customWidget.setEnabled(False)

    def toJson(self):
        raise NotImplemented("You forgot to implement to_json for this instance of Optional Field")

    def isValid(self):
        raise NotImplemented("You forgot to implement isValid for this instance of Optional Field")

    def setIsValid(self, function):
        self.isValid = function

    def setToJson(self, method):
        self.toJson = method


def bold_string(text_to_bold):
    return "<b>" + text_to_bold + "</b>"


class BooleanField(QWidget, JsonSerializable):

    def __init__(self, checkBoxPrompt: str, booleanJsonKey: str):
        super().__init__()
        self.layout = QHBoxLayout()
        self.checkBox = QCheckBox(checkBoxPrompt)
        self.layout.addWidget(self.checkBox)
        self.setLayout(self.layout)
        self.booleanJsonKey = booleanJsonKey

    def toJson(self):
        return {self.booleanJsonKey: self.checkBox.isChecked()}

    def isValid(self):
        return None
