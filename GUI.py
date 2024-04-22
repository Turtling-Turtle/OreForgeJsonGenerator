import json
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
        self.item_type_combo = None
        self.description_QLineEdit = None
        self.speed_label = None
        self.price_field = None
        self.shop_checkbox = None
        self.tier_combo_box = None
        self.description_hbox = None
        self.id = None
        self.name_QLineEdit = None
        self.layout = None
        self.setWindowTitle("Ore Forge Item Creator")
        self.setFixedSize(800, 250)
        # self.setWindowIcon(QIcon("icon.png"))
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.essentials_hbox = QHBoxLayout()
        self.generate_button = QPushButton("Generate Item")

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

        self.essentials_hbox.addWidget(self.generate_button, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.item_type_combo.currentIndexChanged.connect(self.on_item_type_changed)

        # Print button:

        # Grid layout for item attributes
        self.layout.addLayout(self.essentials_hbox)
        self.essentials_hbox.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.create_common_ui()

        self.generate_button.clicked.connect(lambda: self.print_json_data())
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
        self.name_hbox = QHBoxLayout()
        self.name_hbox.addWidget(QLabel(bold_string("Name:")))
        self.name_QLineEdit = QLineEdit()
        self.name_hbox.addWidget(self.name_QLineEdit, Qt.AlignmentFlag.AlignLeft)
        self.layout.addLayout(self.name_hbox)

        # id
        self.id_hbox = QHBoxLayout()

        self.id = generate_item_id()
        self.id_hbox.addWidget(QLabel(bold_string("ID:") + "\t" + self.id),
                               Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.layout.addLayout(self.id_hbox)

        # Description Field
        self.description_hbox = QHBoxLayout()
        self.description_hbox.addWidget(QLabel(bold_string("Description:")))
        self.description_QLineEdit = QLineEdit()
        self.description_hbox.addWidget(self.description_QLineEdit, Qt.AlignmentFlag.AlignLeft)
        self.layout.addLayout(self.description_hbox)

        # Tier Field
        self.tier_hbox = QHBoxLayout()
        self.tier_hbox.addWidget(QLabel(bold_string("Tier:")))
        self.tier_combo_box = QComboBox()
        for tier in valid_tiers:
            self.tier_combo_box.addItem(tier[3])
        self.tier_hbox.addWidget(self.tier_combo_box, Qt.AlignmentFlag.AlignLeft)
        self.layout.addLayout(self.tier_hbox)

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
        self.speed_label = QLabel(bold_string("Conveyor Speed:"))
        self.speed_line = QLineEdit()
        hbox.addWidget(self.speed_label)
        hbox.addWidget(self.speed_line)
        self.layout.addLayout(hbox, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        hbox.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

    def get_data(self):
        item_data = {
            "name": self.name_QLineEdit.text(),
            "id": self.id,
            "description": self.description_QLineEdit.text(),
            "tier": self.tier_combo_box.currentText() if self.tier_combo_box is not None else "null",
            "isShopItem": str(self.shop_checkbox.isChecked()).lower() if self.shop_checkbox is not None else "null",
            "itemValue": self.price_field.text() if (
                        self.shop_checkbox.isChecked() and self.price_field is not None) else "null"
        }
        item_data.update(self.get_item_specific_data())
        return item_data

    def get_item_specific_data(self):
        text = self.item_type_combo.currentText()
        if text == "Dropper":
            return self.get_dropper_data()
        elif text == "Furnace":
            return self.get_furnace_data()
        elif text == "Upgrader":
            return self.get_upgrader_data()
        elif text == "Conveyor":
            return self.get_conveyor_data()
        else:
            return {}

    def get_dropper_data(self):
        pass

    def get_furnace_data(self):
        pass

    def get_upgrader_data(self):
        pass

    def get_conveyor_data(self):
        data = {
            "blockLayout": [
                [1, 1],
                [1, 1]
            ],
            "conveyorSpeed": self.speed_line.text()
        }
        return data

    def print_json_data(self):
        data = self.get_data()
        json_data = json.dumps(data, indent=4)
        print(json_data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ItemCreator()
    win.show()
    sys.exit(app.exec())
