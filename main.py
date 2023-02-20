"""
Script for managing hot reloading of the project.
For more details see the documentation page -

https://kivymd.readthedocs.io/en/latest/api/kivymd/tools/patterns/create_project/

To turn off the hot reload, just change the value of DEBUG to False
"""

import importlib
import os

from kivy import Config
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivymd.tools.hotreload.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager

import View.screens
from Model.database import DataBase

Config.set("graphics", "multisamples", 0)
os.environ["KIVY_GL_BACKEND"] = "angle_sdl2"

LabelBase.register(
    name="Poppins-Regular", fn_regular="assets/fonts/Poppins/Poppins-Regular.ttf"
)
LabelBase.register(
    name="Poppins-SemiBold", fn_regular="assets/fonts/Poppins/Poppins-SemiBold.ttf"
)
LabelBase.register(
    name="Poppins-Medium", fn_regular="assets/fonts/Poppins/Poppins-Medium.ttf"
)
LabelBase.register(
    name="Poppins-Italic", fn_regular="assets/fonts/Poppins/Poppins-Italic.ttf",
)
LabelBase.register(
    name="Poppins-MediumItalic", fn_regular="assets/fonts/Poppins/Poppins-MediumItalic.ttf",
)
LabelBase.register(
    name="Poppins-Bold", fn_regular="assets/fonts/Poppins/Poppins-Bold.ttf"
)


class CalorAide(MDApp):
    """_summary_

    Args:
        DEBUG (bool): The switch indicator for hot reloading.
        KV_DIRS (list[str]): The directory path to the kivy files.
    """

    DEBUG = False
    KV_DIRS = [os.path.join(os.getcwd(), "View")]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.database = DataBase()
        self.manager_screens = MDScreenManager()

    def build_app(self, *_) -> MDScreenManager:
        # theme style whether 'Dark' or 'Light'
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style_switch_animation_duration = 0.5

        # primary pallette for widgets
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.primary_hue = "400"

        # accent pallette for widgets
        self.theme_cls.accent_palette = "DeepPurple"
        self.theme_cls.accent_hue = "800"

        # widgets material style
        self.theme_cls.material_style = "M3"

        self.database = DataBase()
        self.manager_screens = MDScreenManager()

        importlib.reload(View.screens)
        screens = View.screens.screens

        for name_screen, value in screens.items():
            model = value["model"](self.database)
            controller = value["controller"](model)

            screen_names = name_screen.split(",")
            for i, view in enumerate(controller.get_views()):
                view.name = screen_names[i]
                self.manager_screens.add_widget(view)

        return self.manager_screens

    def on_start(self, *_):
        with open("username.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
            username = lines[0]

        file_size = os.path.getsize("username.txt")

        if self.database.username != username:
            self.manager_screens.current = "login screen"
            self.database.username = username

        if file_size != 0 and username != ' ':
            self.manager_screens.current = "home screen"


if __name__ == "__main__":
    # adjust this base on your screen
    Window.size = (360, 640)
    # Window.top = 50
    Window.left = 1160
    CalorAide().run()
