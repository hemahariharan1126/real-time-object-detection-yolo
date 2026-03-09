import cv2
import time
from camera import Camera
from detector import Detector
from utils.visualization import draw_detections, draw_fps

def main():
    # Initialize camera and detector
    cam = Camera(0)
    detector = Detector()
    
    print("Starting detection... Press 'q' in the window to quit.")
    
    prev_time = time.time()
    
    try:
        while True:
            ret, frame = cam.get_frame()
            if not ret:
                print("Failed to grab frame.")
                break
                
            # Perform detection
            results = detector.detect(frame)
            detections = detector.get_detections(results)
            
            # Draw results
            frame = draw_detections(frame, detections)
            
            # Calculate and draw FPS
            curr_time = time.time()
            fps = 1 / (curr_time - prev_time)
            prev_time = curr_time
            frame = draw_fps(frame, fps)
            
            # Display frame
            cv2.imshow("Real-Time YOLOv8", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    finally:
        cam.release()
        cv2.destroyAllWindows()
        print("Camera released and windows closed.")

if __name__ == "__main__":
    main()
