import cv2

from core.image import Image
from core.image_editor import ImageEditor

RESOURCES_DIR = 'resources/'
OUTPUT_DIR = '{}{}'.format(RESOURCES_DIR, 'output/')
ORIGINAL = '{}{}'.format(RESOURCES_DIR, 'photo_of_shirt_ORIGINAL.jpg')


def test_image_constructor():
    image = Image(cv2.imread(ORIGINAL))

    assert image.shape[0] == 3024
    assert image.shape[1] == 3024
    assert image.shape[2] == 3
    assert image.rect == [302, 302, 2419, 2419]


def test_rect_creation():
    image = ImageEditor.load_image(ORIGINAL)
    actual_rect = image.rect
    expected_rect = [302, 302, 2419, 2419]
    assert actual_rect == expected_rect


def test_edit_rect():
    image = ImageEditor.load_image(ORIGINAL)
    assert image.rect == [302, 302, 2419, 2419]

    image.rect = [10, 10, 500, 500]
    assert image.rect == [10, 10, 500, 500]


def test_initialize_with_rect():
    rect = [10, 10, 500, 500]
    image = ImageEditor.load_image(ORIGINAL, rect)

    assert image.rect == [10, 10, 500, 500]

