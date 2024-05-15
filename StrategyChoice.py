from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QComboBox, QLabel, QWidget, QVBoxLayout, QPushButton

from GUI_Upgrade_Strategies import BasicUpgrade, BundledUpgrade, ConditionalUpgrade, InfluencedUpgrade, \
    ResetterUpgrade, ApplyEffect, DestroyOre, CooldownUpgrade, IncrementalUpgrade
from CustomWidgets import JsonSerializable

from GUI_Ore_Effects import BurningOreEffect, FrostBiteOreEffect, UpgradeOreEffect, BundledOreEffect


def bold_string(textToBold):
    return "<b>" + textToBold + "</b>"


class StrategyChoiceField(QWidget, JsonSerializable):
    """
    Takes a dict of strategies and their constructors.
    Each class in the dict should implement the __str__ method
    """

    def __init__(self, strategies: dict, label: str):
        super().__init__()
        self.menu = QComboBox()
        self.label = QLabel(label)
        self.label.setFont(QFont(bold_string("Arial"), 14))
        self.strategies = strategies

        for key, value in strategies.items():
            self.menu.addItem(key.__str__(self))

        self.layout = QVBoxLayout()
        self.hboxLayout = QVBoxLayout()
        self.heldStrategy = None
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.menu)
        self.layout.addLayout(self.hboxLayout)
        self.menu.currentIndexChanged.connect(lambda: self.updateFields())
        self.updateFields()
        self.setLayout(self.layout)

    def clearStrategyWidgets(self):
        for i in reversed(range(self.hboxLayout.count())):
            item = self.hboxLayout.itemAt(i)
            widget = item.widget()
            if isinstance(widget, tuple(self.strategies.items())):
                self.hboxLayout.removeWidget(widget)
                widget.deleteLater()

    def setLabelName(self, label_name):
        self.label.setText(label_name)

    def updateAlignment(self):
        self.hboxLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

    def updateFields(self):
        self.clearStrategyWidgets()
        for key, value in self.strategies.items():
            if key.__str__(self) == self.menu.currentText():
                self.heldStrategy = value()
                self.hboxLayout.addWidget(self.heldStrategy)
                self.updateAlignment()

    def toJson(self):
        return self.heldStrategy.toJson()

    def isValid(self):
        return self.heldStrategy.isValid()

    def clear(self):
        pass


class Bundle(QWidget, JsonSerializable):
    """
    Takes a tuple which contains all info for the strategy of that type.
    tuple must contain these params:
    [0] Display Name of Strategy
    [1] RealName of Strategy
    [2] JsonFieldName of Strategy (EX: upgradeName, effectName)
    [3] listName (EX: upgStrat + x, effect + x)
    [4] Dict of Constructors for each strategy
    """

    def __init__(self, strategies: tuple[str, str, str, str, dict]):
        super().__init__()
        self.strategyInfo = strategies
        self.strategies = strategies[4]
        self.listOfStrategies = []
        self.count = 0

        self.layout = QVBoxLayout()

        self.adderButton = QPushButton("Add new " + strategies[0])
        self.adderButton.clicked.connect(lambda: self.addStrategy())
        self.deleteButton = QPushButton("Delete " + strategies[0])
        self.deleteButton.clicked.connect(lambda: self.deleteStrategy())
        self.setLayout(self.layout)
        self.addStrategy()

    def addStrategy(self):
        strategy = StrategyChoiceField(self.strategies, self.strategyInfo[0])
        self.count += 1
        strategy.label.setText(self.strategyInfo[0] + str(self.count))
        self.layout.addWidget(strategy)
        self.listOfStrategies.append(strategy)

        self.bindButtons()

    def deleteStrategy(self):
        if self.count > 0:
            self.count -= 1
            last = self.listOfStrategies[-1]
            self.listOfStrategies.remove(last)
            self.layout.removeWidget(last)
            last.deleteLater()
            self.bindButtons()

    def bindButtons(self):
        if self.count > 1:
            self.deleteButton.show()
        else:
            self.deleteButton.hide()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.deleteButton)
        self.layout.addWidget(self.adderButton)

    def toJson(self):
        data = {
            self.strategyInfo[2]: self.strategyInfo[1]
        }
        count = 1
        for strategy in self.listOfStrategies:
            data[self.strategyInfo[3] + str(count)] = strategy.toJson()
            count += 1
        return data

    def clear(self):
        pass

    def isValid(self):
        results = []
        for strategy in self.listOfStrategies:
            result = strategy.isValid()
            if result is not None:
                results.append(result)
        return results if len(results) > 0 else None

    def __str__(self):
        return "Bundled " + self.strategyInfo[0]


"""
Dictionary of currently completed UpgradeStrategies and their respective constructors
"""
upgradeStrategies = {
    BasicUpgrade: BasicUpgrade,
    BundledUpgrade: BundledUpgrade,
    ConditionalUpgrade: ConditionalUpgrade,
    InfluencedUpgrade: InfluencedUpgrade,
    ResetterUpgrade: ResetterUpgrade,
    ApplyEffect: ApplyEffect,
    DestroyOre: DestroyOre,
    # CooldownUpgrade: CooldownUpgrade,
    # IncrementalUpgrade: IncrementalUpgrade
}

"""
Dictionary of currently completed OreEffects and their respective constructors
"""
oreEffects = {
    BurningOreEffect: BurningOreEffect,
    FrostBiteOreEffect: FrostBiteOreEffect,
    BundledOreEffect: BundledOreEffect,
    UpgradeOreEffect: UpgradeOreEffect,
}

"""
Tuple For Bundle version of upgrade Strategies
"""
oreEffectInfo = (
    "Ore Effect", "ore.forge.Strategies.OreEffects.BundledOreEffect", "effectName", "effect", oreEffects)

"""
Tuple for Bundle version of ore effects.
"""
upgradeStrategyInfo = (
    "Upgrade", "ore.forge.Strategies.UpgradeStrategies.BundledUpgrade", "upgradeName", "upgStrat",
    upgradeStrategies)
