import numpy as np
from integrated_system import IntegratedFishProcessingSystem

if __name__ == "__main__":
    system_params = {
        'L1': 300,
        'L2': 250,
        'z_range': (0, 200),
        'servo_pins': {
            'theta1': 17,
            'theta2': 18,
            'z': 27
        }
    }

    system = IntegratedFishProcessingSystem(system_params)

    try:
        fish_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        task = system.process_fish_image(fish_image, target_weight=40)
        fish_position = np.array([200, 100, 50])
        system.execute_cutting_task(task, fish_position)
    except Exception as e:
        print(f"錯誤: {e}")
    finally:
        system.cleanup()

