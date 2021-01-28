"""
Remove the background from your photos!
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class PicFix(toga.App):

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        main_box = toga.Box(style=Pack(direction=COLUMN))

        name_label = toga.Label(
            'Your name: ',
            style=Pack(padding=(0, 5))
        )
        self.name_input = toga.TextInput(style=Pack(flex=1))

        name_box = toga.Box(style=Pack(direction=ROW, padding=5))
        name_box.add(name_label)
        name_box.add(self.name_input)

        button = toga.Button(
            'Say Hello!',
            on_press=self.say_hello,
            style=Pack(padding=5)
        )

        main_box.add(name_box)
        main_box.add(button)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box

        self.main_window.open_file_dialog(title=x, initial_directory=x, file_types=x, multiselect=False)
        self.main_window.show()

    def say_hello(self, widget):
        if self.name_input.value:
            name = self.name_input.value
        else:
            name = 'stranger'

        self.main_window.info_dialog(
            'Hi there!',
            "Hello, {}".format(name)
        )

    def action_open_file_dialog(self, widget):
        try:
            fname = self.main_window.open_file_dialog(
                title="Open file with Toga",
                multiselect=False
            )
            if fname is not None:
                self.label.text = "File to open:" + fname
            else:
                self.label.text = "No file selected!"
        except ValueError:
            self.label.text = "Open file dialog was canceled"


def main():
    return PicFix()

----
"""
Remove the background from your photos!
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER
from typing import List

# from picfix.image import Image
from travertino.constants import AQUAMARINE

from src.picfix.image import Image


class PicFix(toga.App):

    def __init__(self, file_list: List[str] = None, image: toga.Image = None, edited_image: Image = None):
        self.file_list = file_list
        self.image = image
        self.edited_image = edited_image
        super().__init__()

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """

        self.main_window = toga.MainWindow(title=self.formal_name)

        # Label to show responses
        self.label = toga.Label('Ready.', style=Pack(padding_top=20))

        # Button
        btn_style = Pack(flex=1)
        btn_open = toga.Button('Select Photo', on_press=self.action_open_file_dialog, style=btn_style)

        # ImageView Box
        image_from_path = toga.Image('resources/pride-brutus.png')
        imageview_from_path = toga.ImageView(image_from_path)
        imageview_from_path.style.update(height=72)
        box.add(imageview_from_path)

        imageview_box = toga.Box(style=Pack(padding=40, background_color=AQUAMARINE))
        imageview_box.style.update(alignment=CENTER)
        imageview_box.style.update(direction=COLUMN)
        imageview_box.add(self.action_show_image)

        # Outermost Box
        box = toga.Box(
            children=[btn_open,
                      imageview_box,
                      self.label],
            style=Pack(
                flex=1,
                direction=COLUMN,
                padding=10
            )
        )

        # Add the content on the Main Window
        self.main_window.content = box

        # Show the main window
        self.main_window.show()

    def action_open_file_dialog(self, widget):
        try:
            image_location = self.main_window.open_file_dialog(
                title="Open file with Toga",
                multiselect=False
            )
            if image_location is not None:
                self.label.text = "File to open:" + image_location
                self.image = toga.Image(image_location)
            else:
                self.label.text = "No file selected!"

        except ValueError:
            self.label.text = "Open file dialog was canceled"

    def action_show_image(self, widget):
        if self.image is None:
            raise ValueError("No image has been provided.")
        imageview = toga.ImageView(self.image)
        imageview.style.update(height=72)
        return imageview

    def action_save_file_dialog(self, widget):
        fname = 'Toga_file.txt'
        try:
            save_path = self.main_window.save_file_dialog(
                "Save file with Toga",
                suggested_filename=fname)
            if save_path is not None:
                self.label.text = "File saved with Toga:" + save_path
            else:
                self.label.text = "Save file dialog was canceled"
        except ValueError:
            self.label.text = "Save file dialog was canceled"


def main():
    return PicFix()

