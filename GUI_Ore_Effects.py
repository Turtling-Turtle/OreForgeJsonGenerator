from PyQt6.QtWidgets import QWidget, QVBoxLayout

import CustomWidgets
import StrategyChoice
from CustomWidgets import JsonSerializable


class BundledOreEffect(QWidget, JsonSerializable):

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.bundle = StrategyChoice.Bundle(StrategyChoice.oreEffectInfo)
        self.layout.addWidget(self.bundle)

    def isValid(self):
        return self.bundle.isValid()

    def toJson(self):
        return self.bundle.toJson()

    def __str__(self):
        return "Bundled Ore Effect"


class BurningOreEffect(QWidget, JsonSerializable):

    def __init__(self):
        super().__init__()
        self.durationField = CustomWidgets.InputField("Duration", isFloat=True)
        self.tempField = CustomWidgets.InputField("Temperature Increase", isFloat=True)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.durationField)
        self.layout.addWidget(self.tempField)
        self.setLayout(self.layout)

    def toJson(self):
        data = {
            "effectName": "ore.forge.Strategies.OreEffects.Burning",
            "duration": self.durationField.toJson(),
            "tempIncrease": self.tempField.toJson(),
        }
        return data

    def isValid(self):
        results = [
            self.durationField.isValid(),
            self.tempField.isValid(),
        ]
        for result in results:
            if result is not None:
                return result
        return

    def __str__(self):
        return "Burning"


class FrostBiteOreEffect(QWidget, JsonSerializable):

    def __init__(self):
        super().__init__()
        self.durationField = CustomWidgets.InputField("Duration:", isFloat=True)
        self.tempField = CustomWidgets.InputField("Temperature Decrease:", isFloat=True)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.durationField)
        self.layout.addWidget(self.tempField)
        self.setLayout(self.layout)

    def toJson(self):
        data = {
            "effectName": "ore.forge.Strategies.OreEffects.FrostBite",
            "duration": self.durationField.toJson(),
            "tempDecrease": self.tempField.toJson(),
        }
        return data

    def isValid(self):
        results = [
            self.durationField.isValid(),
            self.tempField.isValid(),
        ]
        for result in results:
            if result is not None:
                return result
        return

    def __str__(self):
        return "Frost Bite"


class UpgradeOreEffect(QWidget, JsonSerializable):

    def __init__(self):
        super().__init__()
        self.durationField = CustomWidgets.InputField("Duration:", isFloat=True)
        self.interval = CustomWidgets.InputField("Activation Interval:", isFloat=True)
        self.upgrade = StrategyChoice.StrategyChoiceField(StrategyChoice.upgradeStrategies, "Upgrade")
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.durationField)
        self.layout.addWidget(self.interval)
        self.layout.addWidget(self.upgrade)
        self.setLayout(self.layout)

    def toJson(self):
        data = {
            "effectName": "ore.forge.Strategies.OreEffects.UpgradeOreEffect",
            "duration": self.durationField.toJson(),
            "interval": self.interval.toJson(),
            "upgrade": self.upgrade.toJson(),
        }
        return data

    def isValid(self):
        results = [
            self.durationField.isValid(),
            self.interval.isValid(),
            self.upgrade.isValid(),
        ]
        for result in results:
            if result is not None:
                return result
        return

    def __str__(self):
        return "Upgrade Ore Effect"
