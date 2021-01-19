import numpy as np


class Image(object):

    def __init__(self, image, rect=None):
        self.image = image
        self.rect = rect if rect else self.deduce_rect()

    def deduce_rect(self):
        """Creates foreground rectangle.

        Returns:
            list: [x,y,w,h]
        """
        width, height, _ = self.image.shape
        rect_x = int(np.floor(width * 0.1))
        rect_y = int(np.floor(height * 0.1))
        rect_width = int(np.floor(width * 0.8))
        rect_height = int(np.floor(height * 0.8))
        return [rect_x, rect_y, rect_width, rect_height]