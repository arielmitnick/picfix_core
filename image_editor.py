import cv2
import numpy as np


class ImageEditor(object):

    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)

    def remove_background(self, image, iter_count=5):
        """Place image on a white background.

        Args:
            image (PIL.Image): Image to be edited
            iter_count: Number of iterations of GrabCut algorithm to run

        Returns:
            PIL.Image: edited image
        """
        mask = np.zeros(image.shape[:2], np.uint8)
        mask = cv2.grabCut(image, mask, tuple(image.rect), self.bgd_model, self.fgd_model,
                           iterCount=iter_count, mode=cv2.GC_INIT_WITH_RECT)

        mask = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
        image[mask == 0, :] = [255, 255, 255]

        return image

    @staticmethod
    def save_image(location, image):
        cv2.imwrite(location, image)

    @staticmethod
    def resize_image(image, scale_percent=10):
        """Resize an image.

        Args:
            image (picfix.Image): Image object
            scale_percent (int): Percent by which image is resized. 100 represents current size of image.
            If scale_percent is greater than 100, image will be enlarged. If scale_percent is less than 100,
            image will be shrunk.

        Returns:
            cv2.: resized image
        """
        # calculate the 50 percent of original dimensions
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)

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
        return cv2.resize(image, dsize, interpolation)

