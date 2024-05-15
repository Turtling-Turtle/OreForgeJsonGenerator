import json


# https://www.reddit.com/r/Python/comments/v040jf/handling_json_files_with_ease_in_python/
# https://www.100daysofdata.com/python-json

class Item:
    def __init__(self, data: dict):
        self.name = data['name']
        self.id = data['id']
        self.blockLayout = data['blockLayout']
        self.tier = data['tier']
        self.isShopItem = data['isShopItem']
        self.itemValue = data['itemValue']

    def setName(self, name: str):
        self.name = name

    def __str__(self):
        return self.name

    def asDict(self):
        raise NotImplemented(self.__str__() + " needs to implement this method")


class Furnace(Item):
    def __init__(self, data: dict):
        super().__init__(data)
        self.specialPointReward = data.get("specialPointReward")
        self.rewardThreshold = data.get("rewardThreshold")
        self.upgrade = data.get("upgrade")

    def asDict(self):
        return {"name": self.name, "id": self.id, "blockLayout": self.blockLayout, "tier": self.tier,
                "isShopItem": self.isShopItem,
                "itemValue": self.itemValue, "specialPointReward": self.specialPointReward,
                "rewardThreshold": self.rewardThreshold,
                "upgrade": self.upgrade}


class Dropper(Item):
    def __init__(self, data):
        super().__init__(data)

    def asDict(self):
        pass

    pass


class Upgrader(Item):
    def __init__(self, data):
        super().__init__(data)

    def asDict(self):
        pass
    pass


class Conveyor(Item):
    def __init__(self, data):
        super().__init__(data)

    def asDict(self):
        pass

    pass


testFileOutput = "testOutput.json"


def loadItemFile(file: str):
    items = []
    with open(file, 'r') as listOfData:
        data = json.load(listOfData)
        data.remove(data[0])  # Remove version field.
        for item in data:
            items.append(Furnace(item))
        for item in items:
            try:
                print(item)
            except TypeError:
                pass
        print("Changing Names Now!")
        count = 0
        for item in items:
            try:
                count += 1
                item.setName("New Name " + str(count))
            except TypeError:
                pass
        output = []
        for item in items:
            output.append(item.asDict())
        json.dump(output, open(testFileOutput, "w"), indent=1)


loadItemFile("testInput.json")
