import os

import cv2

from image import Image
from image_editor import ImageEditor
from test.test_utils import mse

RESOURCES_DIR = 'resources/'
OUTPUT_DIR = '{}{}'.format(RESOURCES_DIR, 'output/')
BACKGROUND_REMOVED_EXPECTED = '{}{}'.format(RESOURCES_DIR, 'photo_of_shirt_background_removed.jpg')
RESIZED_10_EXPECTED = '{}{}'.format(OUTPUT_DIR, 'resized_10_EXPECTED.jpg')
RESIZED_10_TEST = '{}{}'.format(OUTPUT_DIR, 'resized_10_TEST.jpg')


def test_rect_creation():
    image_location = 'resources/photo_of_shirt_ORIGINAL.jpg'
    image = Image(cv2.imread(image_location))
    actual_rect = image.rect
    expected_rect = [302, 302, 2419, 2419]
    assert actual_rect == expected_rect


def test_edit_rect():
    image_location = 'resources/photo_of_shirt_ORIGINAL.jpg'
    image = Image(cv2.imread(image_location))
    assert image.rect == [302, 302, 2419, 2419]

    image.rect = [10, 10, 500, 500]
    assert image.rect == [10, 10, 500, 500]


def test_initialize_with_rect():
    image_location = 'resources/photo_of_shirt_ORIGINAL.jpg'
    rect = [10, 10, 500, 500]
    image = Image(cv2.imread(image_location), rect=rect)
    assert image.rect == [10, 10, 500, 500]

