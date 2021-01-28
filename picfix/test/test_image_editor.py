import os

import cv2
import numpy as np
import pytest

from picfix.src.picfix.image import Image
from picfix.src.picfix.image_editor import ImageEditor
from picfix.test import mse

RESOURCES_DIR = 'resources/'
OUTPUT_DIR = '{}{}'.format(RESOURCES_DIR, 'output/')
ORIGINAL_IMAGE = '{}{}'.format(RESOURCES_DIR, 'photo_of_shirt_ORIGINAL.jpg')
SMALL_IMAGE = '{}{}'.format(RESOURCES_DIR, 'small_image.jpg')
SMALL_MASK = '{}{}'.format(RESOURCES_DIR, 'small_mask.jpg')
MASK_302 = '{}{}'.format(RESOURCES_DIR, 'mask_302.jpg')

RESIZED_10_EXPECTED = '{}{}'.format(OUTPUT_DIR, 'resized_10_EXPECTED.jpg')
RESIZED_10_TEST = '{}{}'.format(OUTPUT_DIR, 'resized_10_TEST.jpg')
MINI_MASK_EXPECTED = '{}{}'.format(OUTPUT_DIR, 'mini_mask_EXPECTED.jpg')
MINI_MASK_TEST = '{}{}'.format(OUTPUT_DIR, 'mini_mask_TEST.jpg')
LARGE_MASK_EXPECTED = '{}{}'.format(OUTPUT_DIR, 'large_mask_EXPECTED.jpg')
LARGE_MASK_TEST = '{}{}'.format(OUTPUT_DIR, 'large_mask_TEST.jpg')
SPECIFIC_SIZE_EXPECTED = '{}{}'.format(OUTPUT_DIR, 'specific_size_EXPECTED.jpg')
SPECIFIC_SIZE_TEST = '{}{}'.format(OUTPUT_DIR, 'specific_size_TEST.jpg')
GC_MASK_EXPECTED = '{}{}'.format(OUTPUT_DIR, 'gc_mask_EXPECTED.jpg')
GC_MASK_TEST = '{}{}'.format(OUTPUT_DIR, 'gc_mask_TEST.jpg')
BACKGROUND_REMOVED_EXPECTED = '{}{}'.format(OUTPUT_DIR, 'background_removed_EXPECTED.jpg')
BACKGROUND_REMOVED_TEST = '{}{}'.format(OUTPUT_DIR, 'background_removed_TEST.jpg')


class TestImageEditor:

    @pytest.fixture(scope="module")
    def editor(self):
        return ImageEditor()

    @pytest.fixture(scope="module")
    def original_image(self, editor):
        return editor.load_image(ORIGINAL_IMAGE)

    @pytest.fixture(scope="module")
    def small_image(self, editor):
        return editor.load_image(SMALL_IMAGE)

    @pytest.fixture(scope="module")
    def small_mask(self, editor):
        return editor.load_image(SMALL_MASK)

    def test_load_image(self, editor):
        gray_image = editor.load_image(SMALL_IMAGE, grayscale=True)
        assert len(gray_image.shape) == 2

        color_image = editor.load_image(SMALL_IMAGE)
        assert len(color_image.shape) == 3

    def test_initialize_bgd_fgd_models(self, editor):
        bgd_model, fgd_model = editor.initialize_bgd_fgd_models()
        expected_bgd = np.zeros((1, 65), np.float64)
        expected_fgd = np.zeros((1, 65), np.float64)

        assert bgd_model.all() == expected_bgd.all()
        assert fgd_model.all() == expected_fgd.all()
        assert bgd_model.all() == fgd_model.all()

    def test_resize_image__downsize(self, editor, original_image):
        try:
            assert original_image.shape[0] == 3024
            assert original_image.shape[1] == 3024

            actual_resized = editor.resize_image_by_factor(original_image)
            assert actual_resized.shape[0] == 302
            assert actual_resized.shape[1] == 302

            editor.save_image(RESIZED_10_TEST, actual_resized)

            actual_resized = editor.load_image(RESIZED_10_TEST)
            expected_resized = editor.load_image(RESIZED_10_EXPECTED)

            assert mse(actual_resized, expected_resized) == 0

        finally:
            os.remove(RESIZED_10_TEST)

    def test_resize_mask_by_factor__enlarge(self, editor, small_mask):
        """ Test resize_mask_by_factor function of the editor. Note that resizing up again will not return the image to its
        exact original size, because of rounding. This is considered correct behavior for this function. If the original
        size is desired, users should use resize_image_to_size.
        """
        try:
            assert small_mask.shape[0] == 151
            assert small_mask.shape[1] == 151

            resized = editor.resize_image_by_factor(small_mask, scale_percent=2000)

            editor.save_image(LARGE_MASK_TEST, resized)

            actual_mask = editor.load_image(LARGE_MASK_TEST)
            expected_mask = editor.load_image(LARGE_MASK_EXPECTED)

            assert mse(actual_mask, expected_mask) == 0
            assert actual_mask.shape[0] == 3020
            assert actual_mask.shape[1] == 3020

        finally:
            os.remove(LARGE_MASK_TEST)

    def test_resize_image_to_specific_size(self, editor, small_image):
        try:
            assert small_image.shape[0] == 302
            assert small_image.shape[1] == 302

            resized = editor.resize_image_to_specific_size(small_image, 3024, 3024)
            editor.save_image(SPECIFIC_SIZE_TEST, resized)

            actual_resized = editor.load_image(SPECIFIC_SIZE_TEST)
            expected_resized = editor.load_image(SPECIFIC_SIZE_EXPECTED)

            assert mse(actual_resized, expected_resized) == 0
            assert actual_resized.shape[0] == 3024
            assert actual_resized.shape[1] == 3024

        finally:
            os.remove(SPECIFIC_SIZE_TEST)

    def test_find_biggest_contour__image(self, editor, original_image):
        grayscale_image = Image(cv2.cvtColor(original_image.image, cv2.COLOR_BGR2GRAY))

        ret, thresh = cv2.threshold(grayscale_image.image, 127, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        biggest_contour = editor.find_biggest_contour(contours)

        assert len(contours) == 2
        assert biggest_contour.size == 40156
        assert cv2.contourArea(biggest_contour) == 9123472.0

    def test_find_biggest_contour__mask(self, editor):
        small_image = editor.load_image(SMALL_IMAGE)
        mask = editor.do_grab_cut__bounded_box(small_image, iter_count=3)

        ret, thresh = cv2.threshold(mask, 127, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        biggest_contour = editor.find_biggest_contour(contours)

        assert len(contours) == 5
        assert biggest_contour.size == 1740
        assert cv2.contourArea(biggest_contour) == 37651.0

    def test_do_grab_cut__bounded_box(self, editor):

        try:
            small_mask = editor.load_image(SMALL_MASK)
            mask = Image(editor.do_grab_cut__bounded_box(small_mask))

            editor.save_image(MINI_MASK_TEST, mask)

            actual_mask = editor.load_image(MINI_MASK_TEST)
            expected_mask = editor.load_image(MINI_MASK_EXPECTED)

            assert mse(actual_mask, expected_mask) == 0

        finally:
            os.remove(MINI_MASK_TEST)

    def test_do_grab_cut__mask(self, editor, small_image):
        try:
            # do GrabCut on image to generate an initial mask
            small_mask = editor.load_image(MASK_302, grayscale=True)
            assert small_mask.shape[0] == small_image.shape[0]

            # do GrabCut using generated mask
            output_mask = editor.do_grab_cut__mask(small_image, small_mask, iter_count=5)

            editor.save_image(GC_MASK_TEST, Image(output_mask))

            actual_mask = editor.load_image(GC_MASK_TEST)
            expected_mask = editor.load_image(GC_MASK_EXPECTED)

            assert mse(actual_mask, expected_mask) == 0

        finally:
            os.remove(GC_MASK_TEST)

    def test_fill_largest_contour_eliminate_others(self, editor):
        image = editor.load_image(RESIZED_10_EXPECTED)
        mask = editor.do_grab_cut__bounded_box(image, iter_count=3)
        all_contours, h = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        external_contours, h2 = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        assert len(all_contours) > len(external_contours)

        output_mask = editor.fill_largest_contour_eliminate_others(mask)
        all_output_contours, h3 = cv2.findContours(output_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        external_output_contours, h4 = cv2.findContours(output_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        assert len(all_output_contours) == len(external_output_contours)

    def test_remove_background(self, editor, original_image):
        try:
            actual_output = editor.remove_background(original_image)

            editor.save_image(BACKGROUND_REMOVED_TEST, actual_output)

            actual = editor.load_image(BACKGROUND_REMOVED_TEST)
            expected = editor.load_image(BACKGROUND_REMOVED_EXPECTED)
            assert mse(actual, expected) == 0

        finally:
            os.remove(BACKGROUND_REMOVED_TEST)