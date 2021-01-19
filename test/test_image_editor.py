import os

import cv2

from image_editor import ImageEditor
from test.test_utils import mse

RESOURCES_DIR = 'resources/'
OUTPUT_DIR = '{}{}'.format(RESOURCES_DIR, 'output/')
BACKGROUND_REMOVED_EXPECTED = '{}{}'.format(RESOURCES_DIR, 'photo_of_shirt_background_removed.jpg')
ORIGINAL_LOCATION = '{}{}'.format(RESOURCES_DIR, 'photo_of_shirt_ORIGINAL.jpg')
RESIZED_10_EXPECTED = '{}{}'.format(OUTPUT_DIR, 'resized_10_EXPECTED.jpg')
RESIZED_10_TEST = '{}{}'.format(OUTPUT_DIR, 'resized_10_TEST.jpg')
RESIZED_150_EXPECTED = '{}{}'.format(OUTPUT_DIR, 'resized_150_EXPECTED.jpg')
RESIZED_150_TEST = '{}{}'.format(OUTPUT_DIR, 'resized_150_TEST.jpg')


def test_resize_image__downsize():
    try:
        image = cv2.imread(ORIGINAL_LOCATION)
        assert image.shape[0] == 3024
        assert image.shape[1] == 3024

        editor = ImageEditor()
        actual_resized = editor.resize_image(image)
        assert actual_resized.shape[0] == 302
        assert actual_resized.shape[1] == 302

        editor.save_image(RESIZED_10_TEST, actual_resized)

        actual_resized = cv2.imread(RESIZED_10_TEST)
        expected_resized = cv2.imread(RESIZED_10_EXPECTED)

        assert mse(actual_resized, expected_resized) == 0

    finally:
        os.remove(RESIZED_10_TEST)


def test_resize_image__enlarge():
    try:
        image = cv2.imread(ORIGINAL_LOCATION)
        assert image.shape[0] == 3024
        assert image.shape[1] == 3024

        editor = ImageEditor()
        actual_resized = editor.resize_image(image, 150)
        assert actual_resized.shape[0] == 4536
        assert actual_resized.shape[1] == 4536

        editor.save_image(RESIZED_150_TEST, actual_resized)

        actual_resized = cv2.imread(RESIZED_150_TEST)
        expected_resized = cv2.imread(RESIZED_150_EXPECTED)

        assert mse(actual_resized, expected_resized) == 0

    finally:
        os.remove(RESIZED_150_TEST)
