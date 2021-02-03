import os
import re
import shutil

import cv2
import pytest

from core.converter import Converter
from core.filetypes import HeifFileType, JpegFileType
from test.test_utils import mse


def test_converter_constructor__good():
    converter = Converter(HeifFileType(), JpegFileType())
    input_filetype = converter.input_filetype
    output_filetype = converter.output_filetype

    assert input_filetype.__eq__(HeifFileType())
    assert output_filetype.__eq__(JpegFileType())


def test_converter_constructor__bad():
    with pytest.raises(ValueError):
        converter_bad = Converter(JpegFileType(), HeifFileType())


def test_cannot_override_input_output_values():
    converter = Converter(HeifFileType(), JpegFileType())
    with pytest.raises(AttributeError):
        converter.input_filetype = JpegFileType()
        converter.output_filetype = HeifFileType()


def test_convert_single_file_to_jpg():
    """ Uses Converter to convert a .heic file to a .jpg file.

    - Reads in an HEIC file
    - Converts to JPG and saves
    - Reads in generated jpg and a saved copy of the correct JPG for this HEIC file
    - Compares Mean Square Error of the two photos, which should be 0 since the photos are identical
    - Deletes the generated jpg file, regardless of test success or failure.

    """
    input_dir = "resources/"
    jpg_dir = input_dir
    filename = "photo_of_shirt.heic"
    generated_jpg = "photo_of_shirt.jpg"
    master_jpg = "photo_of_shirt_ORIGINAL.jpg"

    test_jpg_location = "{}{}".format(jpg_dir, generated_jpg)
    master_jpg_location = "{}{}".format(jpg_dir, master_jpg)

    try:
        converter = Converter(input_filetype=HeifFileType(), output_filetype=JpegFileType())
        converter.convert_single_file_to_jpg(input_dir, jpg_dir, filename)

        # Read in jpg generated above, master copy of JPG
        test_jpg = cv2.imread(test_jpg_location)
        master_jpg = cv2.imread(master_jpg_location)

        # Compare master copy of JPG vs. test-generated copy
        assert mse(master_jpg, test_jpg) == 0

    # Clean up image generated for test
    finally:
        os.remove(test_jpg_location)


def test_convert_directory_files_to_jpg():
    try:
        input_dir = "resources/johnny_was/"
        jpg_dir = "resources/jpeg/"
        converter = Converter(input_filetype=HeifFileType(), output_filetype=JpegFileType())

        # ensure input meets file type expectation (heic)
        input_directory = os.fsencode(input_dir)
        for i, file in enumerate(os.listdir(input_directory)):
            filename = os.fsdecode(file)
            assert re.search(r"\.heic$", filename, re.IGNORECASE)

        # do file conversion
        converter.convert_directory_files_to_jpg(input_dir, jpg_dir)

        input_files = [name for name in os.listdir(input_dir) if os.path.isfile(name)]
        output_files = [name for name in os.listdir(jpg_dir) if os.path.isfile(name)]

        # compare number of input vs output files
        num_input_files = len(input_files)
        num_output_files = len(output_files)

        assert num_input_files == num_output_files

        # check filetype of output files
        jpg_directory = os.fsencode(jpg_dir)
        for i, file in enumerate(os.listdir(jpg_directory)):
            filename = os.fsdecode(file)
            assert re.search(r"\.jpg$", filename, re.IGNORECASE)

        # check names of output vs. input
        input_names_short = [name.replace(".heic", "") for name in input_files]
        output_names_short = [name.replace(".jpg", "") for name in output_files]

        assert sorted(input_names_short) == sorted(output_names_short)

    finally:
        shutil.rmtree(jpg_dir)


