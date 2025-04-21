# -*- coding: utf-8 -*-

from ..QuModLibs.Client import *
from ..QuModLibs.Modules.UI.Client import QUICanvas, QGridData
from ..QuModLibs.Modules.Services.ItemService.Client import ItemData

from Data import *

class IntroduceCanva(QUICanvas):
    def __init__(self, uiNode, parentPath, data):
        # type: (object, str, IntroduceData) -> None
        QUICanvas.__init__(self, uiNode, parentPath)
        self.drawDefName = "xanz_introduce_book.introduct"
        self.data = data

    def onCreate(self):
        self.clearParent()
        QUICanvas.onCreate(self)
        uiNode = self.getUiNode()

        path = uiNode.getScrollViewContentPath(
            self._conPath + "/panel/panel/message/panel/scroll_view"
        )
        uiNode.GetBaseUIControl(path).asLabel().SetText(self.data.message)

        uiNode.GetBaseUIControl(
            self._conPath + "/panel/image"
        ).asImage().SetSprite("textures/ui/fqy_book_ui/introduce/" + self.data.texturePath)

class EntityCanva(QUICanvas):
    def __init__(self, uiNode, parentPath, data):
        # type: (object, str, EntityData) -> None
        QUICanvas.__init__(self, uiNode, parentPath)
        self.drawDefName = "xanz_introduce_book.normal_golem"
        self.entityData = data

    def onCreate(self):
        self.clearParent()
        QUICanvas.onCreate(self)
        uiNode = self.getUiNode()

        path = uiNode.getScrollViewContentPath(
            self._conPath + "/panel/panel/panel/panel(0)/panel/panel/scroll_view"
        )
        uiNode.GetBaseUIControl(path).asLabel().SetText(self.entityData.message1)

        path = uiNode.getScrollViewContentPath(
            self._conPath + "/panel/panel/panel(0)/panel/scroll_view"
        )
        uiNode.GetBaseUIControl(path).asLabel().SetText(self.entityData.message2)

        uiNode.GetBaseUIControl(
            self._conPath + "/panel/panel/panel/panel/panel/image"
        ).asImage().SetSprite(self.entityData.image)

        uiNode.GetBaseUIControl(
            self._conPath + "/panel/panel/panel/panel/panel(0)/image/label"
        ).asLabel().SetText(
            self.entityData.name if self.entityData.name else self.getCNName()
        )

        self.starGrid()

    def getCNName(self):
        comp = clientApi.GetEngineCompFactory().CreateGame(levelId)
        return comp.GetChinese("entity." + self.entityData.identifier + ".name")

    def starGrid(self):
        def func(viewPath, pos):
            uiNode.GetBaseUIControl(viewPath + "/image").asImage().SetSprite(
                "textures/ui/fqy_book_ui" + ("/filledStar" if pos < self.entityData.starCount else "/star_empty")
            )

        self._QGridData = QGridData(
            self._conPath + "/panel/panel/panel/panel(0)/panel(0)/grid",
            False,
            bindFunc=func,
        )
        uiNode = self.getUiNode()
        uiNode.GetBaseUIControl(
            self._QGridData.getRealPath(uiNode)
        ).asGrid().SetGridDimension((5, 1))
        self.listenQGridRender(self._QGridData)

    def onDestroy(self):
        QUICanvas.onDestroy(self)
        self.unListenQGridRender(self._QGridData)

class NormalItemCanva(QUICanvas):
    def __init__(self, uiNode, parentPath, data):
        # type: (object, str, ItemMessageData) -> None
        QUICanvas.__init__(self, uiNode, parentPath)
        self.drawDefName = "xanz_introduce_book.golem_item"
        self.itemRenderPath = "/panel/panel/panel/panel/item_renderer"
        self.itemMessagePath = "/panel/panel(0)/panel/label"
        self.itemNamePath = "/panel/panel/panel/label"
        self.itemMessageData = data

    def onCreate(self):
        self.clearParent()
        QUICanvas.onCreate(self)
        uiNode = self.getUiNode()
        uiNode.GetBaseUIControl(self._conPath + self.itemRenderPath).asItemRenderer().SetUiItem(self.itemMessageData.itemName, self.itemMessageData.aux)
        uiNode.GetBaseUIControl(self._conPath + self.itemMessagePath).asLabel().SetText("§l" + self.itemMessageData.message)
        itemCNName = ItemData.createItemData(self.itemMessageData.itemName).getItemBasicInfo().itemName
        uiNode.GetBaseUIControl(self._conPath + self.itemNamePath).asLabel().SetText(itemCNName)

class RecipeTableCanva(NormalItemCanva):
    def __init__(self, uiNode, parentPath, data):
        NormalItemCanva.__init__(self, uiNode, parentPath, data)
        self.drawDefName = "xanz_introduce_book.recipe"
        self.itemRenderPath = "/panel/panel/panel(0)(0)/image/item_renderer"
        self.itemMessagePath = "/panel/panel(0)/image/label"
        self.itemNamePath = "/panel/panel/panel(0)(0)/label"

    def onCreate(self):
        self.clearParent()
        NormalItemCanva.onCreate(self)
        self.recipeGrid()

    def recipeGrid(self):
        def func(viewPath, pos):
            if pos >= len(resultList):
                return
            itemDict = resultList[pos]
            if itemDict:
                uiNode.GetBaseUIControl(viewPath + "/panel/item_renderer").SetVisible(True)
                uiNode.GetBaseUIControl(viewPath + "/panel/item_renderer").asItemRenderer().SetUiItem(itemDict.get("item"), itemDict.get("data", 0))
            else:
                uiNode.GetBaseUIControl(viewPath + "/panel/item_renderer").SetVisible(False)

        comp = clientApi.GetEngineCompFactory().CreateRecipe(clientApi.GetLevelId())
        recipe = comp.GetRecipesByResult(self.itemMessageData.itemName, "crafting_table", 0, -1)[0]
        pattern = recipe["pattern"]
        key = recipe["key"]
        resultList = []
        for y in pattern:
            for x in y:
                resultList.append(key.get(x, None))
            yLength = len(y)
            if yLength == 1:
                resultList.extend([None]*(3-yLength))
        patternLength = len(pattern)
        if patternLength < 3:
            resultList.extend([None]* 3 * (3-patternLength))

        self._QGridData = QGridData(
            self._conPath + "/panel/panel/panel(0)/grid",
            False,
            bindFunc=func,
        )
        uiNode = self.getUiNode()
        uiNode.GetBaseUIControl(
            self._QGridData.getRealPath(uiNode)
        ).asGrid().SetGridDimension((3, 3))
        self.listenQGridRender(self._QGridData)

class FiredCanva(QUICanvas):
    def __init__(self, uiNode, parentPath, data):
        # type: (object, str, ItemMessageData) -> None
        QUICanvas.__init__(self, uiNode, parentPath)
        self.drawDefName = "xanz_introduce_book.burn"
        self.itemMessageData = data

        self.itemMessagePath = "/panel(1)/panel(0)/image/label"
        self.inputItemRenderPath = "/panel(1)/panel/panel/panel/image/item_renderer"
        self.inputItemNamePath = "/panel(1)/panel/panel/panel/label"
        self.outputItemRenderPath = "/panel(1)/panel/panel/panel(1)(0)/image/item_renderer"
        self.outputItemNamePath = "/panel(1)/panel/panel/panel(1)(0)/label"

    def onCreate(self):
        self.clearParent()
        QUICanvas.onCreate(self)
        uiNode = self.getUiNode()

        inputItemName = self.itemMessageData.itemName
        uiNode.GetBaseUIControl(self._conPath + self.itemMessagePath).asLabel().SetText("§l" + self.itemMessageData.message)
        uiNode.GetBaseUIControl(self._conPath + self.inputItemRenderPath).asItemRenderer().SetUiItem(inputItemName, self.itemMessageData.aux)

        uiNode.GetBaseUIControl(self._conPath + self.inputItemNamePath).asLabel().SetText(self.getCNName(inputItemName))

        comp = clientApi.GetEngineCompFactory().CreateRecipe(levelId)
        outputItemName = comp.GetRecipesByInput(inputItemName, "furnace", self.itemMessageData.aux)[0].get("output")
        uiNode.GetBaseUIControl(self._conPath + self.outputItemRenderPath).asItemRenderer().SetUiItem(outputItemName, 0)
        uiNode.GetBaseUIControl(self._conPath + self.outputItemNamePath).asLabel().SetText(self.getCNName(outputItemName))

    def getCNName(self, itemName):
        """ 获取物品中文名 """
        return ItemData.createItemData(itemName).getItemBasicInfo().itemName
    
    def onDestroy(self):
        QUICanvas.onDestroy(self)

class CanvaMessage:
    """画布信息"""
    def __init__(self, canva, args):
        # type: (type[QUICanvas], BaseData) -> None
        self.canva = canva
        self.args = args

class TabMessage:
    def __init__(self, canvasList, name, icon):
        # type: (list[CanvaMessage], str, str) -> None
        self.list = canvasList
        self.name = name
        self.icon = "textures/ui/fqy_book_ui/tab_icon/" + icon

    def getLen(self):
        return len(self.list)
