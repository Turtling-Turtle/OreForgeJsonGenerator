import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QLineEdit, QCheckBox, QVBoxLayout, \
    QHBoxLayout, QPushButton

from Helper_Functions import valid_tiers
from Item_Constructors import generate_item_id

'''
The Game Plan:
All prompts that are list based(Upgrades, item tier, etc.) can be converted to use a drop down menu using QComboBox.
Prompts that take strings/input from keyboard can be converted to a text box using QLineEdit.
Boolean prompts can be converted to a checkbox.

    For Bundled upgrade Im thinking that theres a button called "add Another..." and you can just click it to add another upgrade.
'''


def bold_string(text_to_bold):
    return "<b>" + text_to_bold + "</b>"


def underline_string(text_to_underline):
    return "<u>" + text_to_underline + "</u>"


def is_enabled(state):
    if state == 2:
        state.setEnabled(True)
    else:
        state.setEnabled(False)


class ItemCreator(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = None
        self.setWindowTitle("Ore Forge Item Creator")
        # self.setFixedSize(600, 650)
        # self.setWindowIcon(QIcon("icon.png"))
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.essentials_hbox = QHBoxLayout()

        # ComboBox to choose item type
        item_type_label = QLabel(bold_string("Item Type:"))
        # layout.addWidget(self.iem_type_label)
        # self.item_type_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.essentials_hbox.addWidget(item_type_label)

        self.item_type_combo = QComboBox()
        self.item_type_combo.addItem("Dropper")
        self.item_type_combo.addItem("Furnace")
        self.item_type_combo.addItem("Upgrader")
        self.item_type_combo.addItem("Conveyor")
        # layout.addWidget(self.item_type_combo)
        self.essentials_hbox.addWidget(self.item_type_combo, Qt.AlignmentFlag.AlignLeft)
        self.item_type_combo.currentIndexChanged.connect(self.on_item_type_changed)

        # Print button:

        # Grid layout for item attributes
        self.layout.addLayout(self.essentials_hbox)
        self.essentials_hbox.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.create_common_ui()
        self.show()

    def on_item_type_changed(self):
        text = self.item_type_combo.currentText()
        self.clear_grid_layout()
        self.create_common_ui()
        if text == "Dropper":
            self.create_dropper_ui()
        elif text == "Furnace":
            self.create_furnace_ui()
        elif text == "Upgrader":
            self.create_upgrader_ui()
        elif text == "Conveyor":
            self.create_conveyor_ui()

    def clear_grid_layout(self):
        for i in reversed(range(self.layout.count())):
            layout_item = self.layout.itemAt(i)
            if layout_item is not None and layout_item != self.essentials_hbox:
                for j in reversed(range(layout_item.count())):
                    widget = layout_item.itemAt(j).widget()
                    if widget is not None:
                        widget.deleteLater()
                self.layout.removeItem(layout_item)

    def create_common_ui(self):
        # Name Field
        name_hbox = QHBoxLayout()
        name_hbox.addWidget(QLabel(bold_string("Name:")))
        name_hbox.addWidget(QLineEdit(), Qt.AlignmentFlag.AlignLeft)
        self.layout.addLayout(name_hbox)

        # id
        id_hbox = QHBoxLayout()
        id_hbox.addWidget(QLabel(bold_string("ID:") + "\t" + generate_item_id()), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.layout.addLayout(id_hbox)

        # Description Field
        description_hbox = QHBoxLayout()
        description_hbox.addWidget(QLabel(bold_string("Description:")))
        description_hbox.addWidget(QLineEdit())
        self.layout.addLayout(description_hbox)

        # Tier Field
        tier_hbox = QHBoxLayout()
        tier_hbox.addWidget(QLabel(bold_string("Tier:")))
        tier_combo_box = QComboBox()
        for tier in valid_tiers:
            tier_combo_box.addItem(tier[3] + " " + tier[2])
        tier_hbox.addWidget(tier_combo_box, Qt.AlignmentFlag.AlignLeft)
        self.layout.addLayout(tier_hbox)

        self.shop_checkbox = QCheckBox("Shop Item")
        self.shop_checkbox.stateChanged.connect(self.toggle_price_field)

        # Price Field (initially hidden)
        self.price_label = QLabel("Price:")
        self.price_field = QLineEdit()
        self.price_field.setEnabled(False)
        price_layout = QHBoxLayout()
        price_layout.addWidget(self.shop_checkbox)
        price_layout.addWidget(self.price_label)
        price_layout.addWidget(self.price_field, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignCenter)
        self.layout.addLayout(price_layout)

        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)



    def toggle_price_field(self, state):
        if state == 2:
            self.price_field.setEnabled(True)
        else:
            self.price_field.clear()
            self.price_field.setEnabled(False)

    def create_dropper_ui(self):

        pass

    def create_furnace_ui(self):

        pass

    def create_upgrader_ui(self):

        pass

    def create_conveyor_ui(self):
        hbox = QHBoxLayout()
        speed_label = QLabel(bold_string("Conveyor Speed:"))
        speed_line = QLineEdit()
        hbox.addWidget(speed_label, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        hbox.addWidget(speed_line, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.layout.addLayout(hbox)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ItemCreator()
    win.show()
    sys.exit(app.exec())
