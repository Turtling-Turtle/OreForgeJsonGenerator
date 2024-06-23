from typing import Union

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout

from GUI.CustomWidgets.CheckBoxField import CheckBoxField
from GUI.CustomWidgets.DropDownMenu import DropDownMenu
from GUI.CustomWidgets.InputField import InputField
from GUI.JsonSerializable import JsonSerializable
from GUI.Validators.NumberValidator import NumberValidator
from GUI.Validators.Validator import ValidationResult

# TODO update Descriptions.
pinnacle = ("Pinnacle" + "-TEMP DESCRIPTION- THE RAREST", "PINNACLE")
exotic = ("Exotic" + "-TEMP DESCRIPTION - 3rd RAREST", "EXOTIC")
prestige = ("Prestige" + "-TEMP DESCRIPTION -5 RAREST", "PRESTIGE")
special = ("Special" + "-TEMP DESCRIPTION- 2nd RAREST", "SPECIAL")
epic = ("Epic" + "-TEMP DESCRIPTION -5th RAREST", "EPIC")
superRare = ("Super Rare" + "-TEMP DESCRIPTION -6th RAREST", "SUPER_RARE")
rare = ("Rare" + " - TEMP DESCRIPTION - 7th RAREST", "RARE")
uncommon = ("Uncommon" + "- TEMP DESCRIPTION - 8th RAREST", "UNCOMMON")
common = ("Common - TEMP DESCRIPTION - 9th RAREST", "COMMON")
tiers = [pinnacle, exotic, special, prestige, epic, superRare, rare, uncommon, common]

specialPoints = "Special Points", "SPECIAL_POINTS"
prestigeLevel = "Prestige Level", "PRESTIGE_LEVEL"
quest = "Quest", "QUEST"
none = "None", "NONE"
unlockMethods = [prestigeLevel, specialPoints, quest, none]

# Currency
cash = "Cash", "CASH"
specialPoints = "Special Points", "SPECIAL_POINTS"
prestigeCurrency = "Prestige Currency", "PRESTIGE_POINTS"
currency = [cash, specialPoints, prestigeCurrency, none]


class AcquisitionInfo(QWidget, JsonSerializable):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.tierDropDown = DropDownMenu("Tier", "tier", tiers)
        self.layout.addWidget(self.tierDropDown)
        self.tierDropDown.dropDown.currentTextChanged.connect(self.onTierChange)

        self.selectedTierConfig = BaseConfig()
        # self.onTierChange()
        self.layout.addWidget(self.selectedTierConfig)
        self.onTierChange()
        self.setLayout(self.layout)

    def toDict(self) -> dict:
        results = self.tierDropDown.toDict()
        results.update(self.selectedTierConfig.toDict())
        return results

    def validate(self) -> Union[ValidationResult, list[ValidationResult]]:
        results = [self.tierDropDown.validate()]
        results.extend(self.selectedTierConfig.validate())
        return results

    def onTierChange(self):
        currentText = self.tierDropDown.dropDown.currentText()
        self.layout.removeWidget(self.selectedTierConfig)
        if currentText == pinnacle[0]:
            self.selectedTierConfig = PinnacleTierConfig()
        elif currentText == exotic[0]:
            self.selectedTierConfig = ExoticTierConfig()
        elif currentText == prestige[0]:
            self.selectedTierConfig = PrestigeTierConfig()
        elif currentText == special[0]:
            self.selectedTierConfig = SpecialTierConfig()
        else:
            self.selectedTierConfig = DefaultTierConfig()
        self.layout.addWidget(self.selectedTierConfig)


class BaseConfig(QWidget, JsonSerializable):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.jsonWidgets = []
        self.rarityField = InputField("Rarity", NumberValidator(float, min_value=0.1, max_value=100), "rarity", float)
        self.layout.addWidget(self.rarityField)
        self.jsonWidgets.append(self.rarityField)

        self.unlockMethod = DropDownMenu("Unlock Method", "unlockMethod", unlockMethods)
        self.layout.addWidget(self.unlockMethod)
        self.jsonWidgets.append(self.unlockMethod)

        self.unlockRequirement = InputField("Unlock Requirement", NumberValidator(int), "unlockRequirement", int)
        self.layout.addWidget(self.unlockRequirement)
        self.jsonWidgets.append(self.unlockRequirement)

        self.currency = DropDownMenu("Currency Type", "currency", currency)
        self.layout.addWidget(self.currency)
        self.jsonWidgets.append(self.currency)

        self.canBeSold = CheckBoxField("Sellable", "canBeSold")
        self.layout.addWidget(self.canBeSold)
        self.jsonWidgets.append(self.canBeSold)
        self.canBeSold.setDisabled(True)

        self.purchasePrice = InputField("Value", NumberValidator(float), "itemValue", float)
        self.layout.addWidget(self.purchasePrice)
        self.jsonWidgets.append(self.purchasePrice)

        self.sellPrice = InputField("Sell Value", NumberValidator(float), "sellPrice", float)
        self.layout.addWidget(self.sellPrice)
        self.jsonWidgets.append(self.sellPrice)

        self.isPrestigeProof = CheckBoxField("Prestige Proof", "isPrestigeProof")
        self.layout.addWidget(self.isPrestigeProof)
        self.isPrestigeProof.setDisabled(True)
        self.jsonWidgets.append(self.isPrestigeProof)

    def toDict(self) -> dict:
        info = {}
        for widget in self.jsonWidgets:
            info.update(widget.toDict())
        return info

    def validate(self) -> Union[ValidationResult, list[ValidationResult]]:
        results = []
        for widget in self.jsonWidgets:
            result = widget.validate()
            if isinstance(result, list):
                results.extend(result)
            else:
                results.append(result)
        return results


class PinnacleTierConfig(BaseConfig):
    def __init__(self):
        super().__init__()
        self.rarityField.setVisible(False)
        self.rarityField.lineEdit.setText("1")

        self.unlockMethod.updateContent([quest])
        self.unlockMethod.setDisabled(True)

        self.unlockRequirement.lineEdit.setText("0")
        self.unlockRequirement.setVisible(False)

        self.currency.dropDown.setCurrentText(none[0])
        self.currency.setDisabled(True)

        self.canBeSold.checkBox.setChecked(False)

        self.purchasePrice.lineEdit.setText("0")
        self.purchasePrice.setVisible(False)
        self.sellPrice.lineEdit.setText("0")
        self.sellPrice.setVisible(False)

        self.isPrestigeProof.checkBox.setChecked(True)


class ExoticTierConfig(BaseConfig):
    def __init__(self):
        super().__init__()
        self.rarityField.setVisible(False)
        self.rarityField.lineEdit.setText("1")

        self.unlockMethod.updateContent([quest])
        self.unlockMethod.setDisabled(True)

        self.unlockRequirement.setVisible(False)
        self.unlockRequirement.lineEdit.setText("0")

        self.currency.updateContent([specialPoints])
        self.currency.setDisabled(True)

        self.canBeSold.checkBox.setChecked(False)

        self.sellPrice.lineEdit.setText("0")
        self.sellPrice.setVisible(False)

        self.isPrestigeProof.checkBox.setChecked(True)


# Problems with this right now. If I ever need to add a field to the widget I have to change abunch of things
class PrestigeTierConfig(BaseConfig):
    def __init__(self):
        super().__init__()
        self.unlockMethod.updateContent([prestigeLevel, quest])
        self.unlockMethod.dropDown.currentTextChanged.connect(self.selectedUnlockMethod)
        self.selectedUnlockMethod()

        self.unlockRequirement.setLineEditToolTip(
            "Enter the Prestige Level that you want this item to enter the loot pool at.")

        self.currency.updateContent([prestigeCurrency])
        self.currency.setDisabled(True)

        self.canBeSold.checkBox.setChecked(True)

        self.isPrestigeProof.checkBox.setChecked(True)
        self.isPrestigeProof.setDisabled(True)

    def selectedUnlockMethod(self):
        selectedMethod = self.unlockMethod.dropDown.currentText()
        if selectedMethod != prestigeLevel[0]:
            self.unlockRequirement.lineEdit.setText("0")
            self.unlockRequirement.setVisible(False)
        else:
            self.unlockRequirement.setVisible(True)


class SpecialTierConfig(BaseConfig):
    def __init__(self):
        super().__init__()
        self.rarityField.setVisible(False)
        self.rarityField.lineEdit.setText("1")

        self.unlockMethod.updateContent(unlockMethods)
        self.unlockMethod.dropDown.currentTextChanged.connect(self.updateUnlockRequirement)

        self.currency.dropDown.setCurrentText(specialPoints[0])
        self.currency.setDisabled(True)

        self.canBeSold.checkBox.setChecked(True)

        self.isPrestigeProof.checkBox.setChecked(True)

    def updateUnlockRequirement(self):
        currentSelection = self.unlockMethod.dropDown.currentText()
        if currentSelection == none[0]:
            pass
        elif currentSelection == specialPoints[0]:
            pass
        elif currentSelection == prestigeLevel[0]:
            pass
        elif currentSelection == quest[0]:
            pass


class DefaultTierConfig(BaseConfig):
    def __init__(self):
        super().__init__()
        self.rarityField.setVisible(False)
        self.rarityField.lineEdit.setText("1")

        self.unlockMethod.updateContent([none, quest])

        self.currency.dropDown.setCurrentText(cash[0])
        self.currency.setDisabled(True)

        self.isPrestigeProof.checkBox.setChecked(False)

