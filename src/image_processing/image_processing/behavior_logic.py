"""Pure scoring helpers for behavior_controller (no ROS imports, so they can be unit tested anywhere)."""
import numpy as np

# Weights used by behavior_controller (the ROS parameters of the same names are not wired up yet).
SIGMOID_K = 15.0
SIGMOID_X0 = 0.67
CONF_WEIGHT = 0.5
AREA_WEIGHT = 0.5


def sigmoid(x, k, x0):
    return 1 / (1 + np.exp(-k * (x - x0)))


def should_process(frame_count, every_n):
    """True when this detection frame should be processed. every_n < 1 is treated as 1 (every frame)."""
    return frame_count % max(1, int(every_n)) == 0


def valid_detections(detections):
    """Detections that have a class name, a positive confidence and a positive pixel area."""
    return [d for d in detections
            if getattr(d, 'class_name', None) and d.confidence > 0.0 and d.pixel_area > 0.0]


def score_detections(detections, k=SIGMOID_K, x0=SIGMOID_X0, conf_weight=CONF_WEIGHT, area_weight=AREA_WEIGHT):
    """Scores every valid detection.

    Returns (valid, scores, best_index): the valid detections, one score each (same order), and the index of the
    highest score. Returns ([], [], None) when nothing is valid.
    """
    valid = valid_detections(detections)
    if not valid:
        return [], [], None

    areas = np.array([d.pixel_area for d in valid], dtype=np.float32)
    max_area = float(np.max(areas))
    scores = []
    for detection, area in zip(valid, areas):
        norm_area = float(area) / (max_area + 1e-6)
        weighted_confidence = sigmoid(detection.confidence, k, x0)
        scores.append(float(conf_weight * weighted_confidence + area_weight * norm_area))

    best_index = max(range(len(scores)), key=lambda i: scores[i])
    return valid, scores, best_index


def build_features(main, best_score):
    """Feature vector for the distance predictor, always describing the chosen (main) detection."""
    height = main.height
    aspect_ratio = main.width / height if height > 0 else 0
    return [main.confidence, main.pixel_area, best_score, main.width, main.height, aspect_ratio]


def normalised_centre_offset(detection, image_width, image_height):
    """(dx, dy) of the box centre from the image centre, each in -1..1. None while the image size is unknown."""
    if not image_width or not image_height:
        return None
    return (
        (detection.x_center - image_width / 2) / (image_width / 2),
        (detection.y_center - image_height / 2) / (image_height / 2),
    )
