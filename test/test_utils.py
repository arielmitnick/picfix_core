import numpy as np


def mse(a, b):
    """Calculates the mean square error of two photos, a and b.

    The Mean Squared Error (MSE) between the two images is the sum of the
    squared difference between the two images. MSE will always be positive.
    The closer the value is to zero, the more similar the images are.

    Note: The two images must have the same dimensions.

    Args:
        a (picfix.Image): Image object to compare
        b (picfix.Image): Second image object to compare

    Returns:
        float: mean squared error between the two images.

    """
    image_a = a.image
    image_b = b.image
    err = np.sum((image_a.astype("float") - image_b.astype("float")) ** 2)
    err /= float(image_a.shape[0] * image_a.shape[1])

    return err
