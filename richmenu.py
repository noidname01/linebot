from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *


class richMenu:
    def __init__(self, line_bot_api, menuSize, menuName, chatBarText):
        """
        params:
            line_bot_api: line bot api with token
            menuSize: tuple, (width,height) to represent the size of menu
            menuName: string, name of this richmenu
            charBarText: string, text which will display in the input bar
        description:
            richMenu, a class that contain all the step to create a simple richmenu
        """

        # Parameters that creating a richmenu needs
        self.line_bot_api = line_bot_api
        self.menuWidth = menuSize[0]
        self.menuHeight = menuSize[1]
        self.menuName = menuName
        self.chatBarText = chatBarText
        self.areas = []

        # The richmenus Id

        self.richMenuId = ""

    def createNewAreas(self, position_x, position_y, width, height, action):
        """
        input:
            position_x: int, x coordinate of the left upper corner of the tappable area 
            position_y: int, y coordinate of the left upper corner of the tappable area 
            width: int, width of tappable area
            height:int, height of tappable area
            action: PostBackAction, the action which will trigger when users tap this area
        output:
            None
        """

        newArea = RichMenuArea(
            bounds=RichMenuBounds(x=position_x, y=position_y,
                                  width=width, height=height),
            action=action
        )

        self.areas.append(newArea)

    def createRichMenu(self):
        rich_menu_to_create = RichMenu(
            size=RichMenuSize(width=self.menuWidth, height=self.menuHeight),
            selected=False,
            name=self.menuName,
            chat_bar_text=self.chatBarText,
            areas=self.areas
        )

        self.richMenuId = self.line_bot_api.create_rich_menu(
            rich_menu=rich_menu_to_create)

    def setRichMenuImage(self, filePath):
        try:
            if filePath[-3:] == "png":
                contentType = "image/png"
            elif filePath[-4:] == "jpeg":
                contentType == "image/jpeg"
        except:
            # TODO
            pass

        with open(filePath, 'rb') as f:
            self.line_bot_api.set_rich_menu_image(
                self.richMenuId, contentType, f)

    def setDefaultRichMenu(self):
        self.line_bot_api.set_default_rich_menu(self.richMenuId)

    def getRichMenuId(self):
        return self.richMenuId

    def setRichMenu(self, data):
        """
        input: dict, contain below infos
            coordinates: list of tuple, (x,y), which represent the position of area
            sizes: list of tuple, (width, height), which represent the size of area
            postBackActions: list of PostBackAction, which will trigger when being tapped
            main: bool, if true, it will set this richmenu to default 
        output:
            None
        description:
            setRichMenu, this function will go through all the process that
            needed in making richmenu
        """
        # First, create a black richmenu instance with name and chatbartext

        # Second, add new areas into richmenu
        for coordinate, size, postBackAction in zip(data.coordinates, data.sizes, data.postBackActions):
            self.createNewAreas(
                coordinate[0], coordinate[1], size[0], size[1], postBackAction)

        # Third, create a richmenu and get its id
        self.createRichMenu()

        # Then set its image
        self.setRichMenuImage(data.img_path)

        # Finally, set it default to line bot api
        if(data.main):
            self.setDefaultRichMenu()


def replaceCurrentRichMenu(line_bot_api, userId, nextState):
    # TODO
    # need to create a map between states and richmenu's id

    stateToRichMenu = []

    nextRichMenuId = stateToRichMenu[nextState]
    line_bot_api.link_rich_menu_to_user(userId, nextRichMenuId)
