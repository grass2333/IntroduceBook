# -*- coding: utf-8 -*-

from Canvas import *

CanvaList = [
    TabMessage(
        [
            CanvaMessage(IntroduceCanva, IntroduceData("image0", """本项目为游戏引导书.
内置引言,物品,实体,熔炉,工作台等页面介绍.
您可以将页面随意穿插在各个tab中,也可以自制ui,增加新的页面.
""")),
            CanvaMessage(IntroduceCanva, IntroduceData("image1", """该项目依赖QuMod运行,感谢@Zero123_为社区做的贡献""")),
        ],
        "新手引导",
        "tab1"
    ),
    TabMessage(
        [
            CanvaMessage(EntityCanva, EntityData("minecraft:zombie", "僵尸", 2, "该页面可以展示实体,僵尸是一只僵尸", image = "textures/ui/fqy_book_ui/entity_image/entity1")),
            CanvaMessage(NormalItemCanva, ItemMessageData("minecraft:diamond", message="该页面可以展示普通物品,钻石是一个钻石")),
            CanvaMessage(RecipeTableCanva, ItemMessageData("minecraft:diamond_sword", message="该页面会自动识别物品合成表,这是钻石剑")),
        ],
        "第二个tab",
        "tab2"
    ),
    TabMessage(
        [
            CanvaMessage(EntityCanva, EntityData("minecraft:zombie", "僵尸2.0", 4, "页面可以随意组装,僵尸是两只僵尸")),
            CanvaMessage(FiredCanva, ItemMessageData("minecraft:iron_ore", message="该页面可以展示烧制物品")),
            CanvaMessage(EntityCanva, 
                         EntityData(
                            "minecraft:wither", "游趣社区", 5, message1= """该项目遵循BSD 3-Clause License,版权归筑梦科技所有.""", message2 = """贡献者:
    B站 先知_芥无忧(主程)
    B站 辰馨Ariao(UI制作)"""))
        ],
        "第三个tab",
        "tab3"
    )
]
