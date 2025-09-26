import numpy as np
import cv2
from typing import List, Optional

class FishProcessingVision:
    """魚類加工電腦視覺檢測系統"""

    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        equalized = cv2.equalizeHist(blurred)
        edges = cv2.Canny(equalized, 50, 150)
        return edges

    def extract_fish_contour(self, processed_image: np.ndarray) -> Optional[np.ndarray]:
        contours, _ = cv2.findContours(processed_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return None
        largest_contour = max(contours, key=cv2.contourArea)
        epsilon = 0.02 * cv2.arcLength(largest_contour, True)
        return cv2.approxPolyDP(largest_contour, epsilon, True)

    def calculate_3d_features(self, contour: np.ndarray) -> dict:
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        x, y, w, h = cv2.boundingRect(contour)
        major_axis, minor_axis = max(w, h), min(w, h)
        eccentricity = major_axis / minor_axis if minor_axis > 0 else 0
        estimated_volume = area * (minor_axis / 2) * 0.8
        return {
            'area': area,
            'perimeter': perimeter,
            'length': major_axis,
            'width': minor_axis,
            'eccentricity': eccentricity,
            'estimated_volume': estimated_volume
        }

    def predict_cutting_points(self, features: dict, target_weight: float) -> List[float]:
        current_volume = features['estimated_volume']
        length = features['length']
        if current_volume <= 0:
            return []
        volume_ratio = np.clip(target_weight / current_volume, 0.1, 0.9)
        length_ratio = volume_ratio ** (1/3)
        cutting_position = length * (1 - length_ratio)
        return [cutting_position]

