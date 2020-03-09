import numpy as np


'''
    Non_maximum Suppression Algorithm in 3D-image
    
    :param boxes: list, object candidates bounding boxes (size:[N, 6])
    :param scores: list, confidence scores for each bounding box (size:[N])
    :param iou_threshold: float
    
    :return: result box with its score after nms operation
'''


def nms_3d(boxes, scores, iou_threshold):
    # if no entry boxes, return empty list
    if len(boxes) == 0:
        return [], []

    # rephrase bounding boxes & confidence scores
    bounding_boxes = np.array(boxes)
    confidence_scores = np.array(scores)

    # coordinates of bounding boxes
    front_bottom_left_x = bounding_boxes[:, 0]
    front_bottom_left_y = bounding_boxes[:, 1]
    front_bottom_left_z = bounding_boxes[:, 2]
    back_top_right_x = bounding_boxes[:, 3]
    back_top_right_y = bounding_boxes[:, 4]
    back_top_right_z = bounding_boxes[:, 5]

    # compute volume of bounding boxes
    volumes = (back_top_right_x - front_bottom_left_x) * (back_top_right_y - front_bottom_left_y) * (back_top_right_z - front_bottom_left_z)

    # sort score in order to extract the most potential bounding box
    order = np.argsort(confidence_scores[:, 0])

    # initialize result bounding box & its score
    res_boxes = []
    res_score = []

    while order.size > 0:
        max_index = order[-1]  # extract the index of the bounding box with the highest score

        # extract result bounding box
        res_boxes.append(boxes[max_index])
        res_score.append(scores[max_index])

        # compute the coordinates of the intersection regions (of the res_box and all other boxes)
        x1 = np.maximum(front_bottom_left_x[max_index], front_bottom_left_x[order[:-1]])
        x2 = np.minimum(back_top_right_x[max_index], back_top_right_x[order[:-1]])

        y1 = np.maximum(front_bottom_left_y[max_index], front_bottom_left_y[order[:-1]])
        y2 = np.minimum(back_top_right_y[max_index], back_top_right_y[order[:-1]])

        z1 = np.maximum(front_bottom_left_z[max_index], front_bottom_left_z[order[:-1]])
        z2 = np.minimum(back_top_right_z[max_index], back_top_right_z[order[:-1]])
        # [x1, y1, z1] is the front_bottom_left point of the intersection region
        # [x2, y2, z2] is the back_top_right point of the intersection region

        # compute the volume of intersection region
        w = np.maximum(0, x2 - x1)
        h = np.maximum(0, y2 - y1)
        d = np.maximum(0, z2 - z1)

        intersection_volume = w * h * d

        # compute the volume ratio between intersection region and the union of the two ounding boxes
        ratio = intersection_volume / (volumes[max_index] + volumes[order[:-1]] - intersection_volume)

        # delete the bounding boxes with a higher intersection ratio than iou_threshold
        rest_index = np.where(ratio < iou_threshold)
        order = order[rest_index]

    return res_boxes, res_score
