# -*- coding: utf-8 -*-

# --- 介绍书客户端 ---

from ..QuModLibs.Client import *
from ..QuModLibs.UI import ESNC
from ..QuModLibs.Modules.UI.Client import QUICanvas

from IN import CanvaList
from math import ceil


@ESNC.Binding("xanz_introduce_book.main",{"isHud" : 0})
class MessageBook(ESNC):
    def __init__(self):
        clientApi.GetEngineCompFactory().CreateGame(levelId).SimulateTouchWithMouse(True)
        self.tabPos = 0
        self.page = 0
        self.maxPage = 0
        self.leftCanva = None # type: (QUICanvas)
        self.rightCanva = None # type: (QUICanvas)
        self.updateTab(0)
        self.QuGetScrollGridObject("/panel/tab").redrawLayoutSize(1, 5.5, len(CanvaList))
    
    def getScrollViewContentPath(self, path):
        """ 获取滚动条内容 """
        scrollViewUIControl = self.GetBaseUIControl(path).asScrollView()
        return scrollViewUIControl.GetScrollViewContentPath()

    def updatePage(self):
        """ 更新页面 """
        self.removePage()

        canva = CanvaList[self.tabPos]
        addCount = len(canva.list)%2
        
        self.GetBaseUIControl("/panel/panel/change_page/left_page_label").asLabel().SetText("第%s/%s页"%(2 * self.page + 1, 2 *self.maxPage + 2 - addCount))
        self.GetBaseUIControl("/panel/panel/change_page/righ_page_label").asLabel().SetText("第%s/%s页"%(2 * self.page + 2, 2 *self.maxPage + 2 - addCount))
        self.GetBaseUIControl("/panel/panel/change_page/left_button").SetVisible(self.page > 0)
        self.GetBaseUIControl("/panel/panel/change_page/right_button").SetVisible(self.page < self.maxPage)

        leftMessage = canva.list[2 * self.page]
        self.leftCanva = leftMessage.canva(self, "/panel/panel/left_panel", leftMessage.args)
        self.leftCanva.createControl()
        if self.page != self.maxPage or len(canva.list)%2 == 0:
            rightMessage = canva.list[2 * self.page + 1]
            self.rightCanva = rightMessage.canva(self, "/panel/panel/right_panel", rightMessage.args)
            self.rightCanva.createControl()
            self.GetBaseUIControl("/panel/panel/change_page/righ_page_label").SetVisible(True)
        else:
            self.GetBaseUIControl("/panel/panel/change_page/righ_page_label").SetVisible(False)

    def updateTab(self, tabPos):
        # type: (int) -> None
        """ 更新tab """
        self.tabPos = tabPos
        self.page = 0
        canva = CanvaList[tabPos]
        self.maxPage = int(ceil(canva.getLen()/2.0)) - 1
        self.GetBaseUIControl("/panel/panel(1)/image/label").asLabel().SetText("§l" + canva.name)
        self.updatePage()

    def removePage(self):
        """ 删除页面控件 """
        if self.leftCanva: 
            self.leftCanva.removeControl()

        if self.rightCanva: 
            self.rightCanva.removeControl()

    @ESNC.OnClick("/panel/panel/change_page/left_button")
    def leftButton(self):
        self.page = max(self.page - 1, 0)
        self.updatePage()

    @ESNC.OnClick("/panel/panel/change_page/right_button")
    def rightButton(self):
        self.page = min(self.page + 1, self.maxPage)
        self.updatePage()
    
    @ESNC.OnClick("/panel/panel(2)/button")
    def exit(self):
        self.SetRemove()

    @ESNC.GridRenderAdapter("/panel/tab", True, DelayUpdate = True)
    def TabGrid(self, ViewPath, Pos):
        # type: (str, int) -> None
        """ Tab网格 """
        if Pos >= len(CanvaList):
            self.GetBaseUIControl(ViewPath + "/panel").SetVisible(False)
            return
        canva = CanvaList[Pos]
        self.GetBaseUIControl(ViewPath + "/panel/button/label").asLabel().SetText(canva.name)
        self.GetBaseUIControl(ViewPath + "/panel/button/image").asImage().SetSprite(canva.icon)
        self.QuSetButtonCallback(ViewPath + "/panel/button", lambda: self.updateTab(Pos))

    def Destroy(self):
        self.removePage()
        clientApi.GetEngineCompFactory().CreateGame(levelId).SimulateTouchWithMouse(False)


@Listen(Events.ClientItemTryUseEvent)
def MessageBookClientItemTryUseEvent(args):
    """ 打开UI界面 """
    data = Events.ClientItemTryUseEvent(args)
    if data.itemDict and data.itemDict.get("newItemName") == "minecraft:diamond":
        MessageBook()

