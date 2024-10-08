import json
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QMessageBox, QApplication, QScrollArea, QPushButton

from CLI.Item_Constructors import generate_item_id
from GUI.ItemSpecificWidgets.ConveyorWidget import ConveyorWidget
from GUI.ItemSpecificWidgets.DropperWidget import DropperWidget
from GUI.ItemSpecificWidgets.FurnaceWidget import FurnaceWidget
from GUI.UpgradeStrategyWidgets.ConstructorDictionary import returnUpgradeStrategies
from GUI.UpgradeStrategyWidgets.StrategyChoiceField import StrategyChoiceField
from Stopwatch import Stopwatch, TimeUnit
from GUI.AcquisitionInfo import AcquisitionInfo
from GUI.CustomWidgets.DropDownMenu import DropDownMenu
from GUI.ItemSpecificWidgets.UpgraderWidget import UpgraderWidget
from GUI.JsonSerializable import JsonSerializable
from GUI.UniversalAttributes import UniversalAttributes
from GUI.Validators.Validator import ValidationResult

furnace = ("Furnace", "FURNACE")
dropper = ("Dropper", "DROPPER")
upgrader = ("Upgrader", "UPGRADER")
conveyor = ("Conveyor", "CONVEYOR")
itemTypes = [furnace, dropper, upgrader, conveyor]


class ItemCreator(QWidget):
    def __init__(self):
        super().__init__()
        self.scrollBox = QScrollArea()
        self.jsonWidgets = []
        self.scrollBox.setWidgetResizable(True)

        self.mainLayout = QVBoxLayout(self)

        self.itemType = DropDownMenu("Item Type", "itemType", itemTypes)
        self.itemType.dropDown.currentTextChanged.connect(self.updateItemSpecificInfo)
        self.mainLayout.addWidget(self.itemType, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        self.mainLayout.addWidget(self.scrollBox)

        self.contentWidget = QWidget()
        self.contentLayout = QVBoxLayout(self.contentWidget)
        self.contentLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.universalAttributes = UniversalAttributes()
        self.addJsonWidget(self.universalAttributes)

        self.addJsonWidget(AcquisitionInfo())

        self.itemSpecificInfo = FurnaceWidget()
        self.addJsonWidget(self.itemSpecificInfo)

        self.scrollBox.setWidget(self.contentWidget)

        self.generateButton = QPushButton("Create Item")
        self.generateButton.clicked.connect(self.generateItem)
        self.mainLayout.addWidget(self.generateButton,
                                  alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)

        self.setLayout(self.mainLayout)

    def updateItemSpecificInfo(self) -> None:
        print("Updating Item Specific Info")
        self.removeJsonWidget(self.itemSpecificInfo)
        # self.removeJsonWidget(self.itemSpecificInfo)
        self.universalAttributes.setItemId(generate_item_id())
        itemType = self.itemType.dropDown.currentText()
        if itemType == itemTypes[0][0]:  # Furnace
            self.itemSpecificInfo = FurnaceWidget()
        elif itemType == itemTypes[1][0]:  # Dropper
            self.itemSpecificInfo = DropperWidget()
        elif itemType == itemTypes[2][0]:  # Upgrader
            self.itemSpecificInfo = UpgraderWidget(self.universalAttributes.getItemId())
        elif itemType == itemTypes[3][0]:  # Conveyor
            self.itemSpecificInfo = ConveyorWidget()

        # self.addJsonWidget(self.itemSpecificInfo)
        self.addJsonWidget(self.itemSpecificInfo)
        # self.scrollBox.setWidget(self.contentWidget)

    def addJsonWidget(self, jsonWidget: JsonSerializable):
        self.contentLayout.addWidget(jsonWidget)
        self.jsonWidgets.append(jsonWidget)

    def removeJsonWidget(self, target: JsonSerializable):
        self.contentLayout.removeWidget(target)
        self.jsonWidgets.remove(target)

    def generateItem(self) -> None:
        watch = Stopwatch(TimeUnit.SECONDS)
        watch.start()
        validationResults = self.validateFields()
        errorList = self.verifyResults(validationResults)
        watch.print()
        if len(errorList) > 0:
            self.postError(errorList)
        else:
            print(json.dumps(self.getJSON(), indent=2))

    def getJSON(self) -> dict:
        data = {}
        for widget in self.jsonWidgets:
            if isinstance(widget, UniversalAttributes):
                data.update(widget.toDict())
                data.update(self.getDefaultBlockLayout())
            elif isinstance(widget, JsonSerializable):
                data.update(widget.toDict())
        return data

    def getDefaultBlockLayout(self) -> dict:
        itemType = self.itemType.dropDown.currentText()
        if itemType == itemTypes[0][0]:  # Furnace
            return {"blockLayout": [[4, 4],
                                    [4, 4]
                                    ]}
        elif itemType == itemTypes[1][0]:  # Dropper
            return {"blockLayout": [[0, 3, 0],
                                    [0, 0, 0],
                                    [0, 0, 0]
                                    ]}
        elif itemType == itemTypes[2][0]:  # Upgrader
            return {"blockLayout": [[2, 2],
                                    [1, 1]
                                    ]}
        elif itemType == itemTypes[3][0]:  # Conveyor
            return {"blockLayout": [[1, 1],
                                    [1, 1]
                                    ]}

    def validateFields(self) -> list[ValidationResult]:
        validationResults = []
        for widget in self.jsonWidgets:
            result = widget.validate()
            if isinstance(result, list):
                validationResults.extend(result)
            else:
                validationResults.append(result)
        return validationResults

    def postError(self, errorList: list[str]) -> None:
        error_box = QMessageBox()
        error_box.setWindowTitle("Validation Error")
        error_box.setIcon(QMessageBox.Icon.Critical)
        error_text = "Data validation failed."
        for error in errorList:
            print()
            error_text += "\n" + error
        error_box.setText(error_text)
        error_box.exec()

    def verifyResults(self, validationResults: list[ValidationResult]) -> list:
        errorList = []
        for validationResult in validationResults:
            if validationResult.hasError():
                errorList.append(validationResult.getErrorMessage())
        return errorList


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ItemCreator()
    win.setWindowTitle("Ore Forge Content Manager")
    win.show()
    sys.exit(app.exec())
