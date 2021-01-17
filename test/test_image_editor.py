import os

import cv2

from image_editor import ImageEditor
from test.test_utils import mse


expected_image_location = 'resources/photo_of_shirt_background_removed.jpg'


# def test_image_size():
#     image_location = 'resources/photo_of_shirt_ORIGINAL.jpg'
#     image = cv2.imread(image_location)
#     print(image.shape)
#     assert 1==2

# l = [1, 2, 3, 4]
# x = tuple(l)
# assert x == (1, 2, 3, 4)
#
#


def test_rect_getter():
    image_location = 'resources/photo_of_shirt_ORIGINAL.jpg'
    image = cv2.imread(image_location)
    editor = ImageEditor(image)
    actual_rect = editor.rect
    expected_rect = [302, 302, 2419, 2419]
    assert actual_rect == expected_rect

#TODO: fix rect setter function :(
def test_rect_setter__valid():
    image_location = 'resources/photo_of_shirt_ORIGINAL.jpg'
    image = cv2.imread(image_location)
    editor = ImageEditor(image)
    assert editor.rect == [302, 302, 2419, 2419]

    editor.rect = [10, 10, 500, 500]
    assert editor.rect == [10, 10, 500, 500]


def test_remove_background():
    image_location = 'resources/photo_of_shirt_ORIGINAL.jpg'
    image = cv2.imread(image_location)
    editor = ImageEditor(image)

    image = editor.remove_background(image)
    expected_image = cv2.imread(expected_image_location)

    assert mse(image, expected_image) == 0


def test_save_image():
    try:
        source_location = 'resources/photo_of_shirt_ORIGINAL.jpg'
        image = cv2.imread(source_location)
        editor = ImageEditor(image)
        dest_dir_location = 'resources/output/'
        photo_name = 'photo_of_shirt_background_removed.jpg'
        dest_location = '{}{}'.format(dest_dir_location, photo_name)

        if not os.path.exists(dest_dir_location):
            os.makedirs(dest_dir_location)

        image = editor.remove_background(image)
        editor.save_image(image, dest_location)

        output_files = [name for name in os.listdir(dest_dir_location) if os.path.isfile(name)]
        assert len(output_files) == 1
        assert output_files[0] == 'photo_of_shirt_background_removed_jpg'

        img = cv2.imread(dest_location)
        expected_image = cv2.imread(expected_image_location)

        assert mse(img, expected_image) == 0

    finally:
        pass
        #os.remove(dest_location)
