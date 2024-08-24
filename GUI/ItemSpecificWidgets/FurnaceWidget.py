from PyQt6.QtWidgets import QWidget, QVBoxLayout

from GUI.CustomWidgets.InputField import InputField
from GUI.JsonSerializable import JsonSerializable
from GUI.UpgradeStrategyWidgets.ConstructorDictionary import returnUpgradeStrategies
from GUI.UpgradeStrategyWidgets.StrategyChoiceField import StrategyChoiceField
from GUI.Validators.NumberValidator import NumberValidator


class FurnaceWidget(QWidget, JsonSerializable):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.specialPointReward = InputField("Special Point Reward", NumberValidator(int), "specialPointReward", int)
        self.specialPointThreshold = InputField("Special Point Reward Threshold", NumberValidator(int), "rewardThreshold", int)
        self.layout.addWidget(self.specialPointThreshold)
        self.layout.addWidget(self.specialPointReward)
        self.upgradeStrategy = StrategyChoiceField(returnUpgradeStrategies(), "Sell Bonus ")
        self.layout.addWidget(self.upgradeStrategy)

        self.setLayout(self.layout)
