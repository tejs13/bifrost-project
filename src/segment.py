# created by Patel Tejaskumar
# segment.py

import numpy as np
from skimage import filters, morphology, measure
from skimage.color import label2rgb

def segment_image(image):
    """
    Segment the Image while coloring the objects and attaching ID to objects
    :param image: Image file
    :return:
    """
    # Convert the image to grayscale numpy array
    image_array = np.array(image.convert("L"))
    threshold = filters.threshold_otsu(image_array)
    binary_image = image_array > threshold
    # Cleaned by removing small objects
    cleaned_image = morphology.remove_small_objects(binary_image, min_size=50)
    # Label the objects
    labeled_image = measure.label(cleaned_image)
    # Color the labeled image
    colored_image = label2rgb(labeled_image, image=image_array, bg_label=0)
    return colored_image
