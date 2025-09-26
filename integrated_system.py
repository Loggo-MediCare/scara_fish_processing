import numpy as np
import time
from dataclasses import dataclass
from typing import List
from scara_robot import SCARARobot
from fish_vision import FishProcessingVision

@dataclass
class CuttingTask:
    target_weight: float
    cutting_points: List[float]
    timestamp: float

class IntegratedFishProcessingSystem:
    """結合 SCARA 機器人與魚類視覺處理"""

    def __init__(self, robot_params: dict):
        self.robot = SCARARobot(**robot_params)
        self.vision = FishProcessingVision()
        self.tasks = []

    def process_fish_image(self, image: np.ndarray, target_weight: float) -> CuttingTask:
        processed = self.vision.preprocess_image(image)
        contour = self.vision.extract_fish_contour(processed)
        if contour is None:
            raise ValueError("未檢測到魚類輪廓")
        features = self.vision.calculate_3d_features(contour)
        cutting_points = self.vision.predict_cutting_points(features, target_weight)
        task = CuttingTask(target_weight, cutting_points, time.time())
        self.tasks.append(task)
        return task

    def execute_cutting_task(self, task: CuttingTask, fish_position: np.ndarray):
        print(f"切割任務開始，目標重量 {task.target_weight}g")
        for cut in task.cutting_points:
            target = np.array([fish_position[0] + cut, fish_position[1], fish_position[2]])
            self.robot.move_to(target)
            time.sleep(0.5)
        print("切割完成")

    def cleanup(self):
        self.robot.cleanup()

