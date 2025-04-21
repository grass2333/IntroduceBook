# -*- coding: utf-8 -*-


class BaseData:
    def __init__(self):
        pass

class IntroduceData(BaseData):
    def __init__(self, texturePath="", message="你说得对,但是原神"):
        self.texturePath = texturePath
        self.message = message

class EntityData(BaseData):
    def __init__(self, identifier, name = "", starCount = 0, message1 = "", message2 = "", image = ""):
        self.identifier = identifier
        self.starCount = starCount
        self.name = name
        self.message1 = message1
        self.message2 = message2
        self.image = image

class ItemMessageData(BaseData):
    def __init__(self, itemName, aux = 0, message = ""):
        self.itemName = itemName
        self.aux = aux
        self.message = message
