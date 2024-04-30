from PyQt6.QtWidgets import QWidget

from SubMenu import JsonSerializable


# @author Nathan Ulmen


class BundledOreEffect:

    def __init__(self):
        super().__init__()

    def to_json(self):
        pass

    def isValid(self):
        pass


class BurningOreEffect(QWidget, JsonSerializable):

    def __init__(self):
        super().__init__()

    def to_json(self):
        pass

    def isValid(self):
        pass


class FrostBiteOreEffect(QWidget, JsonSerializable):
    pass

    def __init__(self):
        super().__init__()

    def to_json(self):
        pass

    def isValid(self):
        pass


class UpgradeOreEffect(QWidget, JsonSerializable):

    def __init__(self):
        super().__init__()

    def to_json(self):
        pass

    def isValid(self):
        pass
