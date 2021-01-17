import cv2
import numpy as np


class ImageEditor(object):

    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)

    def __init__(self, image, rect=None):
        self.image = image
        self.rect = rect

    @property
    def rect(self):
        """Getter for foreground rectangle.

        Returns:
            list: [x,y,w,h]
        """
        width, height, _ = self.image.shape
        rect_x = int(np.floor(width * 0.1))
        rect_y = int(np.floor(height * 0.1))
        rect_width = int(np.floor(width * 0.8))
        rect_height = int(np.floor(height * 0.8))
        return [rect_x, rect_y, rect_width, rect_height]

    @rect.setter
    def rect(self, proposed_rect):
        """Place image on a white background.

        Args:
            proposed_rect (list): Rectangle representing definite foreground.

        Returns:
            list: [x,y,w,h]
        """
        x, y, w, h = proposed_rect
        width, height, _ = self.image.shape
        if not ((0 < x < w) and (0 < y < h) and (w < width) and (h < height)):
            raise ValueError("Invalid rectangle for image dimensions.")
        self._rect = proposed_rect

    def remove_background(self, image):
        """Place image on a white background.

        Args:
            image (PIL.Image): Image to be edited

        Returns:
            PIL.Image: edited image
        """
        mask = np.zeros(image.shape[:2], np.uint8)
        cv2.grabCut(image, mask, tuple(self.rect), self.bgd_model, self.fgd_model, iterCount=5,
                    mode=cv2.GC_INIT_WITH_RECT)

        mask_2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
        image[mask_2 == 0, :] = [255, 255, 255]

        return image

    def save_image(self, image, location):
        cv2.imwrite(location, image)
