"""
Remove the background from your photos!
"""
import cv2
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER
from toga.constants import HIDDEN, VISIBLE
from typing import List

from travertino.constants import AQUAMARINE

from src.picfix.image import Image
from src.picfix.image_editor import ImageEditor


class PicFix(toga.App):

    # def __init__(self, file_list: List[str] = None, image: toga.Image = None, edited_image: Image = None):
    #     self.file_list = file_list
    #     self.image = image
    #     self.edited_image = edited_image
    #     super().__init__()

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """

        # Create Buttons
        self.button_hide = toga.Button(
            label='Hide label',
            style=Pack(padding=10, width=120),
            on_press=self.hide_label
        )

        self.button_add = toga.Button(
            label='Add image',
            style=Pack(padding=10, width=120),
            on_press=self.add_image,
        )

        self.button_remove = toga.Button(
            label='Remove image',
            style=Pack(padding=10, width=120),
            on_press=self.remove_image,
            enabled=False,
        )

        self.button_insert = toga.Button(
            label='Insert image',
            style=Pack(padding=10, width=120),
            on_press=self.insert_image,
        )

        self.button_reparent = toga.Button(
            label='Reparent image',
            style=Pack(padding=10, width=120),
            on_press=self.reparent_image,
            enabled=False,
        )

        self.button_add_to_scroll = toga.Button(
            label='Add new label',
            style=Pack(padding=10, width=120),
            on_press=self.add_label,
        )

        self.button_remove_background = toga.Button(
            label='Remove background',
            style=Pack(padding=10, width=120),
            on_press=self.remove_background,
            enabled=False,
        )

        self.scroll_box = toga.Box(children=[], style=Pack(direction=COLUMN, padding=10, flex=1))
        self.scroll_view = toga.ScrollContainer(content=self.scroll_box, style=Pack(width=120))

        self.image = toga.Image('resources/test_image.jpg')
        self.image_view = toga.ImageView(self.image, style=Pack(padding=10, width=60, height=60))
        tf = cv2.haveImageReader('resources/test_image.jpg')
        i = cv2.imread('resources/test_image.jpg')
        print(i)

        # this tests adding children during init, before we have an implementation
        self.button_box = toga.Box(
            children=[
                self.button_hide,
                self.button_add,
                self.button_insert,
                self.button_reparent,
                self.button_remove,
                self.button_add_to_scroll,
                self.button_remove_background,
            ],
            style=Pack(direction=COLUMN),
        )

        self.box = toga.Box(
            children=[],
            style=Pack(direction=ROW, padding=10, alignment=CENTER, flex=1)
        )

        # this tests adding children when we already have an impl but no window or app
        self.box.add(self.button_box)
        self.box.add(self.scroll_view)

        # add a couple of labels to get us started
        self.labels = []
        for i in range(3):
            self.add_label()

        self.main_window = toga.MainWindow()
        self.main_window.content = self.box
        self.main_window.show()

    def hide_label(self, sender):
        if self.labels[0].style.visibility == HIDDEN:
            self.labels[0].style.visibility = VISIBLE
            self.button_hide.label = "Hide label"
        else:
            self.labels[0].style.visibility = HIDDEN
            self.button_hide.label = "Show label"

    def add_image(self, sender):
        self.scroll_box.add(self.image_view)

        self.button_reparent.enabled = True
        self.button_remove.enabled = True
        self.button_remove_background.enabled = True
        self.button_add.enabled = False
        self.button_insert.enabled = False

    def add_edited_image(self, sender):
        self.edited_image = toga.Image('resources/output_image.jpg')
        self.edited_view = toga.ImageView(self.edited_image, style=Pack(padding=10, width=60, height=60))
        self.scroll_box.add(self.edited_view)

        self.button_reparent.enabled = True
        self.button_remove.enabled = True
        self.button_add.enabled = False
        self.button_insert.enabled = False

    def insert_image(self, sender):
        self.scroll_box.insert(1, self.image_view)

        self.button_reparent.enabled = True
        self.button_remove.enabled = True
        self.button_add.enabled = False
        self.button_insert.enabled = False

    def remove_image(self, sender):
        self.image_view.parent.remove(self.image_view)

        self.button_reparent.enabled = False
        self.button_remove.enabled = False
        self.button_add.enabled = True
        self.button_insert.enabled = True

    def reparent_image(self, sender):
        if self.image_view.parent is self.button_box:
            self.scroll_box.insert(0, self.image_view)
        elif self.image_view.parent is self.scroll_box:
            self.button_box.add(self.image_view)

    def remove_background(self, sender):
        editor = ImageEditor()
        print(self.image.path)
        tf = cv2.haveImageReader('resources/test_image.jpg')
        #img = cv2.imread('resources/test_image.jpg')
        print(tf)
        print(type(tf))
        #img = editor.load_image('resources/test_image.jpg')
        #edited_img = editor.remove_background(img)
        # editor.save_image('resources/output_image.jpg', img)
        # self.add_edited_image()
        # self.scroll_box.add(self.edited_view)
        #
        # self.button_remove_background.enabled = False

    def add_label(self, sender=None):
        # this tests adding children when we already have an impl, window and app
        new_label = toga.Label(
            'Label {}'.format(len(self.scroll_box.children)),
            style=Pack(padding=2, width=70)
        )
        self.scroll_box.add(new_label)
        self.labels.append(new_label)

    #####

    # def action_open_file_dialog(self, widget):
    #     try:
    #         image_location = self.main_window.open_file_dialog(
    #             title="Open file with Toga",
    #             multiselect=False
    #         )
    #         if image_location is not None:
    #             self.label.text = "File to open:" + image_location
    #             self.image = toga.Image(image_location)
    #         else:
    #             self.label.text = "No file selected!"
    #
    #     except ValueError:
    #         self.label.text = "Open file dialog was canceled"
    #
    # def action_show_image(self, widget):
    #     if self.image is None:
    #         raise ValueError("No image has been provided.")
    #     imageview = toga.ImageView(self.image)
    #     imageview.style.update(height=72)
    #     return imageview
    #
    # def action_save_file_dialog(self, widget):
    #     fname = 'Toga_file.txt'
    #     try:
    #         save_path = self.main_window.save_file_dialog(
    #             "Save file with Toga",
    #             suggested_filename=fname)
    #         if save_path is not None:
    #             self.label.text = "File saved with Toga:" + save_path
    #         else:
    #             self.label.text = "Save file dialog was canceled"
    #     except ValueError:
    #         self.label.text = "Save file dialog was canceled"


def main():
    return PicFix()
