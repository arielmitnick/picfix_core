from filetypes import SupportedFileTypes, JpegFileType, HeifFileType


def test_filetype__jpeg_init():
    ft = JpegFileType()
    assert ft.file_type == SupportedFileTypes.JPEG
    assert ft.supported_as_input is True
    assert ft.supported_as_output is True


def test_filetype__heif_init():
    ft = HeifFileType()
    assert ft.file_type == SupportedFileTypes.HEIF
    assert ft.supported_as_input is True
    assert ft.supported_as_output is False
