# tracking.py

import matplotlib
matplotlib.use('Agg')

import numpy as np
import os
from scipy.spatial import distance
from skimage import filters, morphology, measure
from skimage.color import label2rgb
from constants import MAX_DISTANCE, MIN_SIZE_THRESHOLD, OUTPUT_DIR
import matplotlib.pyplot as plt


def track_objects_in_stack(image_stack):
    """
    Track objects while saving position and size in csv for images stream
    :param image_stack: Stack of Images
    :return:
    """
    tracking_data = []
    object_ids = {}
    next_id = 1
    frame_index = 0
    while True:
        try:
            image = np.array(image_stack.convert("L"))
            threshold = filters.threshold_otsu(image)
            binary_image = image > threshold
            cleaned_image = morphology.remove_small_objects(binary_image, min_size=50)
            labeled_image = measure.label(cleaned_image)
            properties = measure.regionprops(labeled_image)
            current_objects = {}

            # Prepare to color the labeled image for visualization
            colored_image = label2rgb(labeled_image, image=image, bg_label=0)

            for prop in properties:
                position = prop.centroid
                size = prop.area

                if size < MIN_SIZE_THRESHOLD:
                    continue

                matched_id = None
                min_dist = float('inf')
                for obj_id, prev_position in object_ids.items():
                    dist = distance.euclidean(position, prev_position)
                    if dist < MAX_DISTANCE and dist < min_dist:
                        min_dist = dist
                        matched_id = obj_id

                if matched_id is None:
                    matched_id = next_id
                    next_id += 1

                current_objects[matched_id] = position

                tracking_data.append({
                    'Object Index': len(tracking_data) + 1,
                    'Object Id': matched_id,
                    'Position': position,
                    'Size': size,
                    'Frame No': frame_index
                })

                # Update the labeled image with the assigned object ID
                labeled_image[labeled_image == prop.label] = matched_id

            object_ids = current_objects

            # Create a figure to overlay the IDs
            fig, ax = plt.subplots(figsize=(8, 8))
            ax.imshow(colored_image)
            for obj_id, pos in current_objects.items():
                y, x = pos
                ax.text(x, y, str(obj_id), color="white", fontsize=12, ha="center", va="center", weight="bold")

            # Save the labeled image with tracked object IDs
            labeled_image_path = os.path.join(OUTPUT_DIR, f'labeled_frame_{frame_index}.png')
            plt.axis('off')  # Hide axes
            plt.savefig(labeled_image_path, bbox_inches='tight', pad_inches=0)
            plt.close(fig)  # Close the figure to free memory
            print(f"Labeled image saved for frame {frame_index} as labeled_frame_{frame_index}.png")
            frame_index += 1
            image_stack.seek(frame_index)

        except EOFError:
            break

    return tracking_data
