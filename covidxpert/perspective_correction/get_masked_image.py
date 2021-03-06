import numpy as np
import cv2

def get_masked_image(image: np.ndarray):
    # Applying the threshold
    _, thresholded_mask = cv2.threshold(image, image.min(), 255, cv2.THRESH_BINARY)

    _, output, stats, _ = cv2.connectedComponentsWithStats(
        thresholded_mask,
        connectivity=8
    )

    image_mask = np.zeros((output.shape), dtype=np.uint8)
    image_mask[output == np.argmax(stats[1:, -1]) + 1] = 255

    # We determine the contours of the mask
    contours, _ = cv2.findContours(
        image=image_mask,
        mode=cv2.RETR_TREE,
        method=cv2.CHAIN_APPROX_NONE
    )

    # And fill up the mask within thr contours
    # as they might remain holes within.
    image_mask = cv2.fillPoly(
        image_mask,
        pts=[contours[0]],
        color=255
    )

    # Computing the chull of the mask
    chull = cv2.convexHull(contours[0])

    merged_mask = cv2.fillPoly(image_mask, [chull], 255)

    return merged_mask