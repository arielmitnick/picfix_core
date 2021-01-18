import cv2
import numpy as np


class ImageEditor(object):

    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)

    def __init__(self, image, rect=None):
        self.image = image
        self.rect = rect if rect else self.deduce_rect()
        self.mask = np.zeros(image.shape[:2], np.uint8)

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

    def remove_background(self, image, iter_count=5):
        """Place image on a white background.

        Args:
            image (PIL.Image): Image to be edited

        Returns:
            PIL.Image: edited image
        """
        cv2.grabCut(image, self.mask, tuple(self.rect), self.bgd_model, self.fgd_model, iterCount=5,
                    mode=cv2.GC_INIT_WITH_RECT)

        mask_2 = np.where((self.mask == 2) | (self.mask == 0), 0, 1).astype('uint8')
        image[mask_2 == 0, :] = [255, 255, 255]

        return image

    def save_image(self, location, image):
        cv2.imwrite(location, image)

    def resize_image(self, scale_percent=10):
        """Place image on a white background.

        Args:
            scale_percent (int): Percent by which image is resized. 100 represents current size of image.
            If scale_percent is greater than 100, image will be enlarged. If scale_percent is less than 100,
            image will be shrunk.

        Returns:
            cv2.: resized image
        """
        # calculate the 50 percent of original dimensions
        width = int(self.image.shape[1] * scale_percent / 100)
        height = int(self.image.shape[0] * scale_percent / 100)

        # dsize
        dsize = (width, height)

        # interpolation
        if scale_percent > 100:
            interpolation = cv2.INTER_CUBIC
        elif 0 < scale_percent <= 100:
            interpolation = cv2.INTER_AREA
        else:
            raise ValueError("Negative resize percentages are not supported.")

        # resize image
        return cv2.resize(self.image, dsize, interpolation)

