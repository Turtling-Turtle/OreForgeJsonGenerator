from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QComboBox, QLabel, QWidget, QVBoxLayout, QHBoxLayout

from SubMenu import JsonSerializable, BasicUpgrade, BundledUpgrade, ConditionalUpgrade, InfluencedUpgrade, \
    ResetterUpgrade, ApplyEffect, DestroyOre, CooldownUpgrade, IncrementalUpgrade

upgrades = ["Basic Upgrade", "Bundled Upgrade", "Conditional Upgrade", "Influenced Upgrade", "Resetter Upgrade",
            "Apply Effect", "Destroy Ore", "Cooldown Upgrade", "Incremental Upgrade"]


class UpgradeChoices(QWidget, JsonSerializable):

    def __init__(self):
        super().__init__()
        self.menu = QComboBox()
        self.label = QLabel("Upgrade:")
        for upgrade in upgrades:
            self.menu.addItem(upgrade)
        self.layout = QHBoxLayout()
        self.hboxLayout = QVBoxLayout()
        self.held_upgrade = None
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.menu)
        self.layout.addLayout(self.hboxLayout)



        self.menu.currentIndexChanged.connect(lambda: self.update_fields())
        # self.layout.addWidget(self.held_upgrade)
        self.update_fields()
        self.setLayout(self.layout)

    def clear_upgrade_widgets(self):
        for i in reversed(range(self.hboxLayout.count())):
            item = self.hboxLayout.itemAt(i)
            widget = item.widget()
            if isinstance(widget, (BasicUpgrade, BundledUpgrade, ConditionalUpgrade, InfluencedUpgrade, ResetterUpgrade, ApplyEffect, DestroyOre, CooldownUpgrade, IncrementalUpgrade)):
                self.hboxLayout.removeWidget(widget)
                widget.deleteLater()

    def update_fields(self):
        selected = self.menu.currentText()
        self.clear_upgrade_widgets()
        if selected == upgrades[0]:
            self.held_upgrade = BasicUpgrade()
            self.hboxLayout.addWidget(self.held_upgrade)
            self.hboxLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
            pass
        elif selected == upgrades[1]:
            self.held_upgrade = BundledUpgrade()
            self.hboxLayout.addWidget(self.held_upgrade)
            self.hboxLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
            pass
        elif selected == "Conditional Upgrade":
            # Code for Conditional Upgrade
            pass
        elif selected == "Influenced Upgrade":
            # Code for Influenced Upgrade
            pass
        elif selected == "Restter Upgrade":
            # Code for Restter Upgrade
            pass
        elif selected == "Apply Effect":
            # Code for Apply Effect
            pass
        elif selected == "Destroy Ore":
            # Code for Destroy Ore
            pass
        elif selected == "Cooldown Effect":
            # Code for Cooldown Effect
            pass
        elif selected == "Incremental Upgrade":
            # Code for Incremental Upgrade
            pass

    def to_json(self):
        return self.held_upgrade.to_json()



