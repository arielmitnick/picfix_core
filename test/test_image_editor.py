import os

import cv2

from image_editor import ImageEditor
from test.test_utils import mse

RESOURCES_DIR = 'resources/'
OUTPUT_DIR = '{}{}'.format(RESOURCES_DIR, 'output/')
BACKGROUND_REMOVED_EXPECTED = '{}{}'.format(RESOURCES_DIR, 'photo_of_shirt_background_removed.jpg')
RESIZED_10_EXPECTED = '{}{}'.format(OUTPUT_DIR, 'resized_10_EXPECTED.jpg')
RESIZED_10_TEST = '{}{}'.format(OUTPUT_DIR, 'resized_10_TEST.jpg')


def test_rect_creation():
    image_location = 'resources/photo_of_shirt_ORIGINAL.jpg'
    image = cv2.imread(image_location)
    editor = ImageEditor(image)
    actual_rect = editor.rect
    expected_rect = [302, 302, 2419, 2419]
    assert actual_rect == expected_rect


def test_edit_rect():
    image_location = 'resources/photo_of_shirt_ORIGINAL.jpg'
    image = cv2.imread(image_location)
    editor = ImageEditor(image)
    assert editor.rect == [302, 302, 2419, 2419]

    editor.rect = [10, 10, 500, 500]
    assert editor.rect == [10, 10, 500, 500]


def test_initialize_with_rect():
    image_location = 'resources/photo_of_shirt_ORIGINAL.jpg'
    image = cv2.imread(image_location)
    rect = [10, 10, 500, 500]
    editor = ImageEditor(image, rect)

    assert editor.rect == [10, 10, 500, 500]


def test_resize_image():
    try:
        image_location = 'resources/photo_of_shirt_ORIGINAL.jpg'
        image = cv2.imread(image_location)
        editor = ImageEditor(image)
        assert image.shape[0] == 3024
        assert image.shape[1] == 3024

        actual_resized = editor.resize_image()
        assert actual_resized.shape[0] == 302
        assert actual_resized.shape[1] == 302

        editor.save_image(RESIZED_10_TEST, actual_resized)

        actual_resized = cv2.imread(RESIZED_10_TEST)
        expected_resized = cv2.imread(RESIZED_10_EXPECTED)

        assert mse(actual_resized, expected_resized) == 0
    finally:
        os.remove(RESIZED_10_TEST)


