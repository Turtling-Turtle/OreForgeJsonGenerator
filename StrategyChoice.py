from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QComboBox, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QFrame

from SubMenu import JsonSerializable, BasicUpgrade, BundledUpgrade, ConditionalUpgrade, InfluencedUpgrade, \
    ResetterUpgrade, ApplyEffect, DestroyOre, CooldownUpgrade, IncrementalUpgrade

upgrades = ["Basic Upgrade", "Bundled Upgrade", "Conditional Upgrade", "Influenced Upgrade", "Resetter Upgrade",
            "Apply Effect", "Destroy Ore", "Cooldown Upgrade", "Incremental Upgrade"]

oreEffects = [""]


def bold_string(text_to_bold):
    return "<b>" + text_to_bold + "</b>"


upgradeStrategies = {
    BasicUpgrade: BasicUpgrade,
    BundledUpgrade: BundledUpgrade,
    ConditionalUpgrade: ConditionalUpgrade,
    InfluencedUpgrade: InfluencedUpgrade,
    ResetterUpgrade: ResetterUpgrade,
    # ApplyEffect: ApplyEffect,
    DestroyOre: DestroyOre,
    # CooldownUpgrade: CooldownUpgrade,
    # IncrementalUpgrade: IncrementalUpgrade
}

oreEffects = {

}


class StrategyChoice(QWidget, JsonSerializable):
    def __init__(self, strategies):
        super().__init__()
        self.menu = QComboBox()
        self.label = QLabel("Upgrade:")
        self.label.setFont(QFont(bold_string("Arial"), 14))
        self.strategies = strategies

        for key, value in strategies.items():
            self.menu.addItem(key.__str__(self))

        self.layout = QVBoxLayout()
        self.hboxLayout = QVBoxLayout()
        self.held_strategy = None
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.menu)
        self.layout.addLayout(self.hboxLayout)
        self.menu.currentIndexChanged.connect(lambda: self.update_fields())
        self.update_fields()
        self.setLayout(self.layout)

    def clear_strategy_widgets(self):
        for i in reversed(range(self.hboxLayout.count())):
            item = self.hboxLayout.itemAt(i)
            widget = item.widget()
            if isinstance(widget, tuple(self.strategies.items())):
                self.hboxLayout.removeWidget(widget)
                widget.deleteLater()

    def set_label_name(self, label_name):
        self.label.setText(label_name)

    def update_alignment(self):
        self.hboxLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

    def update_fields(self):
        self.clear_strategy_widgets()
        for key, value in self.strategies.items():
            if key.__str__(self) == self.menu.currentText():
                self.held_strategy = value()
                self.hboxLayout.addWidget(self.held_strategy)
                self.update_alignment()

    def to_json(self):
        return self.held_strategy.to_json()

    def isValid(self):
        return self.held_strategy.isValid()
