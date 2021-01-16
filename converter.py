import os

import pyheif
from PIL import Image


class Converter(tuple):

    """Converts files from input type to output type.

    If the class has public attributes, they may be documented here
    in an ``Attributes`` section and follow the same formatting as a
    function's ``Args`` section. Alternatively, attributes may be documented
    inline with the attribute's declaration (see __init__ method below).

    Properties created with the ``@property`` decorator should be documented
    in the property's getter method.

    Attributes:
        input_filetype (str): Starting filetype
        output_filetype (str): Desired filetype

    """

    def __new__(cls, input_filetype, output_filetype):
        if input_filetype.supported_as_input and output_filetype.supported_as_output:
            return tuple.__new__(cls, (input_filetype, output_filetype))
        else:
            raise ValueError("Combination of input type {} and output type {} is not supported.".format(
                input_filetype, output_filetype))

    @property
    def input_filetype(self):
        return self[0]

    @property
    def output_filetype(self):
        return self[1]

    def __setattr(self, *ignored):
        raise NotImplementedError

    def __delattr__(self, *ignored):
        raise NotImplementedError

    def convert_directory_files_to_jpg(self, input_dir, jpg_dir=None):
        """Convert files in a directory to jpeg format.

        Args:
            input_dir (str): Directory holding input. Should include ending "/".
            jpg_dir (str): Directory for JPEG output. Should include ending "/". If not specified, defaults to
            creating a new directory inside input_dir.

        Returns:
            bool: outputs photos as JPEG to jpg_dir, returns True if successful, else False.
        """
        if jpg_dir is None:
            jpg_dir = "jpeg/"

        # create output directory if it does not exist yet
        if not os.path.exists(jpg_dir):
            os.makedirs(jpg_dir)

        input_directory = os.fsencode(input_dir)
        for item in os.listdir(input_directory):
            filename = os.fsdecode(item)
            self.convert_single_file_to_jpg(input_dir, jpg_dir, filename)

    def convert_single_file_to_jpg(self, input_dir, jpg_dir, filename):
        """Convert individual file to jpeg format.

        Args:
            input_dir (str): Directory holding input.
            jpg_dir (str): Directory for JPEG output.
            filename (str): Name of file to be converted.

        Returns:
            bool: The return value. True for success, False otherwise.
        """
        file_path = "{}{}".format(input_dir, filename)
        heif_file = pyheif.read(file_path)
        image = Image.frombytes(
            heif_file.mode,
            heif_file.size,
            heif_file.data,
            "raw",
            heif_file.mode,
            heif_file.stride,
        )

        jpg_name = filename.replace(".heic", ".jpg")
        jpg_path = "{}{}".format(jpg_dir, jpg_name)
        image.save(jpg_path, "JPEG")
