from enum import Enum

BASE_LOCATION = "/Users/ariel/Desktop/"


class SupportedFileTypes(Enum):
    JPEG = "jpeg"
    JPG = "jpeg"
    HEIC = "heif"
    HEIF = "heif"


class FileType(object):

    # TODO: Do not allow initialization of FileType directly - only through subclasses
    def __init__(self, file_type, supported_as_input=False, supported_as_output=False):
        self.file_type = file_type
        self.supported_as_input = supported_as_input
        self.supported_as_output = supported_as_output


class JpegFileType(FileType):

    def __init__(self, supported_as_input=True, supported_as_output=True):
        super().__init__(SupportedFileTypes.JPEG, supported_as_input, supported_as_output)


class HeifFileType(FileType):

    def __init__(self, supported_as_input=True, supported_as_output=False):
        super().__init__(SupportedFileTypes.HEIF, supported_as_input, supported_as_output)
