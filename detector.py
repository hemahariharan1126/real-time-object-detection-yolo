from ultralytics import YOLO
import torch

class Detector:
    def __init__(self, model_path='yolov8n.pt', task='detect'):
        """
        Initialize the YOLOv8 detector.
        :param model_path: Path to the .pt model file.
        :param task: Model task (e.g., 'detect', 'segment').
        """
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"Using device: {self.device}")
        
        # Load the model (this will download it automatically if not found)
        self.model = YOLO(model_path)
        self.model.to(self.device)

    def detect(self, frame, conf=0.25):
        """
        Perform optimized object detection.
        :param frame: Input image.
        :param conf: Confidence threshold.
        """
        # img_size 640 is standard, but smaller can be faster (e.g. 320 or 416)
        # Use stream=True for generator behavior or just standard predict
        results = self.model.predict(
            source=frame, 
            conf=conf, 
            verbose=False, 
            imgsz=640,  # Keeping 640 for accuracy, can reduce to 320 for speed
            half=(self.device == 'cuda')  # FP16 inference if GPU
        )
        return results[0]

    def get_detections(self, results):
        """
        Extract bounding boxes and labels from results.
        :param results: Results object from YOLO.predict.
        :return: List of detections (box, score, class_id, label).
        """
        detections = []
        for box in results.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            conf = box.conf[0].item()
            cls = int(box.cls[0].item())
            label = self.model.names[cls]
            detections.append({
                'bbox': [int(x1), int(y1), int(x2), int(y2)],
                'confidence': float(conf),
                'class_id': cls,
                'label': label
            })
        return detections

if __name__ == "__main__":
    # Simple test for detector
    import cv2
    import numpy as np
    
    detector = Detector()
    # Create a dummy blank image
    dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    results = detector.detect(dummy_frame)
    print(f"Detector initialized and ran on dummy frame. Names: {detector.model.names[:5]}")
