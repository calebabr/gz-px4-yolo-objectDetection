import numpy as np
from collections import deque
from typing import List, Optional, Tuple
from models.schemas import Detection, Pose, ImageMetadata, ProminentObject, ProminentObjectArray, FeaturesResponse

class BehaviorProcessor:
    def __init__(self):
        self.history = deque(maxlen=5)
        self.objects = {
            "casual_female": {
                "class": "person",
                "position": np.array([-10.618467534215167, -7.4531963026138293, 0])
            },
        }
        # Default parameters
        self.k = 15.0
        self.x0 = 0.67
        self.conf_weight = 0.5
        self.area_weight = 0.5

    def sigmoid(self, x: float, k: float, x0: float) -> float:
        return 1 / (1 + np.exp(-k * (x - x0)))

    def compute_correct_prominent(self, drone_pos: np.ndarray) -> Tuple[Optional[str], float, Optional[str]]:
        min_dist = float('inf')
        closest_name, closest_class = None, None
        for name, info in self.objects.items():
            dist = np.linalg.norm(drone_pos - info["position"])
            if dist < min_dist:
                min_dist = dist
                closest_name = name
                closest_class = info["class"]
        return closest_name, min_dist, closest_class

    def process_detections(self, detections: List[Detection], drone_pos: np.ndarray, image_metadata: ImageMetadata, history: Optional[List[Detection]] = None) -> dict:
        if history:
            self.history.extend(history)

        if not detections:
            raise ValueError("No detections provided")

        # Filter valid detections
        valid_dets = []
        areas = []
        confs = []
        for det in detections:
            if det.confidence <= 0.0 or det.pixel_area <= 0.0:
                continue
            areas.append(det.pixel_area)
            confs.append(det.confidence)
            valid_dets.append(det)

        if not valid_dets:
            raise ValueError("No valid detections")

        areas = np.array(areas, dtype=np.float32)
        confs = np.array(confs, dtype=np.float32)
        max_area = np.max(areas) if areas.size > 0 else 1.0

        # Find best detection
        best_idx, best_score = None, -np.inf
        for i, (area, conf) in enumerate(zip(areas, confs)):
            norm_area = area / (max_area + 1e-6)
            norm_conf = conf
            w_conf = self.sigmoid(norm_conf, self.k, self.x0)
            score = self.conf_weight * w_conf + self.area_weight * norm_area
            if score > best_score:
                best_score = score
                best_idx = i

        main = valid_dets[best_idx]
        self.history.append(main)

        # Compute distances
        matching_objs = [obj for obj in self.objects.values() if obj["class"] == main.class_name]
        if matching_objs:
            obj = matching_objs[0]
            distance_x = np.linalg.norm(drone_pos[0] - obj["position"][0])
            distance_y = np.linalg.norm(drone_pos[1] - obj["position"][1])
            distance_z = abs(drone_pos[2] - obj["position"][2])
        else:
            distance_x = distance_y = distance_z = None

        correct_name, correct_dist, correct_class = self.compute_correct_prominent(drone_pos)
        label = 0 if main.class_name == correct_class else 1

        # Smoothed prominent
        classes = [det.class_name for det in self.history]
        most_freq_class = max(set(classes), key=classes.count)
        prominent = next(det for det in reversed(self.history) if det.class_name == most_freq_class)

        # Prominent object
        prominent_obj = ProminentObject(
            class_name=main.class_name,
            x_center=main.x_center,
            y_center=main.y_center,
            size_score=best_score
        )

        # Array of all
        array_msg = ProminentObjectArray(objects=[])
        for det, area, conf in zip(valid_dets, areas, confs):
            norm_area = det.pixel_area / (max_area + 1e-6)
            w_conf = self.sigmoid(det.confidence, self.k, self.x0)
            sc = self.conf_weight * w_conf + self.area_weight * norm_area
            array_msg.objects.append(ProminentObject(
                class_name=det.class_name,
                x_center=det.x_center,
                y_center=det.y_center,
                size_score=sc
            ))

        # Features
        bbox_width = main.width
        bbox_height = main.height
        bbox_aspect_ratio = bbox_width / bbox_height if bbox_height > 0 else 0

        features = [
            main.confidence,
            main.pixel_area,
            best_score,
            bbox_width,
            bbox_height,
            bbox_aspect_ratio,
        ]

        features_resp = FeaturesResponse(features=features)

        return {
            "prominent_detection": prominent,
            "prominent_object": prominent_obj,
            "prominent_array": array_msg,
            "features": features_resp,
            "label": label,
            "distance_x": distance_x,
            "distance_y": distance_y,
            "distance_z": distance_z
        }