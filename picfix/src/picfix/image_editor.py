import cv2
import numpy as np

from src.picfix.image import Image


class ImageEditor(object):

    @staticmethod
    def initialize_bgd_fgd_models():
        bgd_model = np.zeros((1, 65), np.float64)
        fgd_model = np.zeros((1, 65), np.float64)
        return bgd_model, fgd_model

    @staticmethod
    def load_image(location, rect=None, grayscale=False):
        print(location)
        flags = cv2.IMREAD_GRAYSCALE if grayscale else None
        return Image(cv2.imread(location, flags=flags), rect)

    @staticmethod
    def save_image(location, image):
        """Resize an image.

        Args:
            location (str): Path to image file
            image (picfix.Image): Image object.
        """
        cv2.imwrite(location, image.image)

    @staticmethod
    def resize_image_by_factor(image, scale_percent=10):
        """Resize an image by a factor.

        Note that resizing up again will not return the image to its exact original size, because of rounding. This
        is considered correct behavior for this function. If the original size is desired, users should use
        resize_image_to_size instead.

        Args:
            image (picfix.Image): Image object
            scale_percent (int): Percent by which image is resized. 100 represents current size of image.
            If scale_percent is greater than 100, image will be enlarged. If scale_percent is less than 100,
            image will be shrunk.

        Returns:
            picfix.Image: Image resized by factor.
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
        return Image(cv2.resize(image.image, dsize, interpolation))

    @staticmethod
    def resize_image_to_specific_size(image, desired_width, desired_height):
        """Resize an image, specifying the desired width and height.

        Resizes an image to a specific size, either larger or smaller than the original image.

        Args:
            image (picfix.Image): Image object
            desired_width (int): Desired width of resized image
            desired_height (int): Desired height of resized image

        Returns:
            Filled in mask
        """
        # Select correct algorithm. If stretching image,
        if desired_width >= image.shape[1] and desired_height >= image.shape[0]:
            interpolation = cv2.INTER_CUBIC
        elif desired_width <= image.shape[1] and desired_height <= image.shape[0]:
            interpolation = cv2.INTER_AREA
        else:
            interpolation = cv2.INTER_LINEAR

        # resize image
        return Image(cv2.resize(image.image, (desired_width, desired_height), interpolation=interpolation))

    @staticmethod
    def find_biggest_contour(contours):
        """Finds largest contour, given the contours of an image.

        Args:
            contours (list(point vectors)): Image to be edited. Note that this is a picfix Image, which wraps
                PIL.Image.

        Returns:
            point vector: the largest contour in the input list.
        """

        biggest_contour = max(contours, key=cv2.contourArea)
        return biggest_contour

    def do_grab_cut__bounded_box(self, image, iter_count=5):
        """Performs GrabCut algorithm using an input bounding rectangle auto calculated from the image.

        Args:
            image (picfix.Image): Image to be edited. Note that this is a picfix Image, which wraps
                PIL.Image.
            iter_count: Number of iterations of GrabCut algorithm to run

        Returns:
            mask: mask representing background/foreground division
        """
        # initialize bgd_model, fgd_model, and mask
        bgd_model, fgd_model = self.initialize_bgd_fgd_models()
        mask = np.zeros(image.shape[:2], np.uint8)

        # set seed to 0 to ensure deterministic result
        cv2.setRNGSeed(0)
        mask, _, _ = cv2.grabCut(image.image, mask, tuple(image.rect), bgd_model, fgd_model,
                                 iterCount=iter_count, mode=cv2.GC_INIT_WITH_RECT)

        output_mask = np.where((mask == 2) | (mask == 0), 0, 1)
        output_mask = (output_mask * 255).astype("uint8")

        return output_mask

    def do_grab_cut__mask(self, image, mask, iter_count=5):
        """Performs GrabCut algorithm, given an input mask.

        Args:
            image (picfix.Image): Image to be edited. Note that this is a picfix Image, which wraps
                PIL.Image.
            mask (picfix.Image - binary): Mask for grabcut algorithm.
            iter_count: Number of iterations of GrabCut algorithm to run

        Returns:
            mask: mask representing background/foreground division
        """
        bgd_model, fgd_model = self.initialize_bgd_fgd_models()

        mask = mask.image
        mask[mask > 0] = cv2.GC_PR_FGD
        mask[mask == 0] = cv2.GC_PR_BGD

        cv2.setRNGSeed(0)
        mask, _, _ = cv2.grabCut(image.image, mask, None, bgd_model, fgd_model,
                                 iterCount=iter_count, mode=cv2.GC_INIT_WITH_MASK)
        output_mask = np.where((mask == 2) | (mask == 0), 0, 1)
        output_mask = (output_mask * 255).astype("uint8")

        return output_mask

    def fill_largest_contour_eliminate_others(self, mask):
        """Fills largest contour in a mask (binary image) white, while blacking out everything else.

        Given a mask (binary image), this method will detect the largest contour and fill it in with white. Then,
        contours are re-computed, and remaining contours are filled in with black. The result is a completely filled
        in white outline of the primary object on a completely black background.

        Args:
            mask (PIL.Image): Image to be edited. Note that this is a PIL.Image.

        Returns:
            mask: A refined mask with one completely white shape and the rest black
        """
        copy_mask = mask.copy()
        contours, hierarchy = cv2.findContours(copy_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        biggest_contour = self.find_biggest_contour(contours)

        # fill largest contour with white, eliminating holes inside it
        cv2.fillConvexPoly(mask, biggest_contour, color=(255, 255, 255))

        # get contours from filled image, which have changed
        mask_copy_2 = mask.copy()
        new_contours, new_hierarchy = cv2.findContours(mask_copy_2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        biggest_contour = self.find_biggest_contour(new_contours)
        other_contours = [c for c in new_contours if c is not biggest_contour]

        # fill other contours with black, making them invisible
        for contour in other_contours:
            cv2.fillConvexPoly(mask, contour, color=(0, 0, 0))

        return mask

    def remove_background(self, image):
        """Place image on a white background.

        The approach here is to generate an initial mask guess for the image by doing GrabCut on a small version of
        the original image and re-enlarging that to the image's original size. Then, we run GrabCut on the original
        image. Finally, the largest contour (presumed the object) is filled in on the mask, all other external contours
        are filled in black, and the mask is applied to the original image, yielding a white background.

        Args:
            image (picfix.Image): Image to be edited. Note that this is a picfix Image, which wraps
                PIL.Image.

        Returns:
            picfix.Image: edited image
        """

        # shrink image to 5% of original
        minified = self.resize_image_by_factor(image, scale_percent=10)

        # do GrabCut on resized image to generate an initial mask
        mini_mask = self.do_grab_cut__bounded_box(minified, iter_count=3)

        # enlarge mask to original size of image
        full_size_mask = self.resize_image_to_specific_size(Image(mini_mask), image.shape[1], image.shape[0])

        # use re-enlarged mask as mask for GrabCut on original image
        output_mask = self.do_grab_cut__mask(image, full_size_mask, iter_count=5)

        # fill the largest contour, then black out remaining contours
        output_mask = self.fill_largest_contour_eliminate_others(output_mask)

        # apply mask to image, setting any black areas of the mask to white in the final image
        image.image[output_mask == 0, :] = [255, 255, 255]

        return image