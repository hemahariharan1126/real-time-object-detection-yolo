import cv2

def draw_detections(frame, detections):
    """
    Draw bounding boxes and labels on the frame.
    :param frame: Image frame from OpenCV.
    :param detections: List of detection dictionaries.
    :return: Annotated frame.
    """
    for det in detections:
        x1, y1, x2, y2 = det['bbox']
        label = f"{det['label']} {det['confidence']:.2f}"
        
        # Draw bounding box
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        # Draw label background
        (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
        cv2.rectangle(frame, (x1, y1 - 20), (x1 + w, y1), (0, 255, 0), -1)
        
        # Draw text
        cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
    
    return frame

def draw_fps(frame, fps):
    """
    Draw FPS text on the frame.
    :param frame: Image frame.
    :param fps: Calculated FPS.
    """
    cv2.putText(frame, f"FPS: {fps:.2f}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    return frame
