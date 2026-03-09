from flask import Flask, render_template, Response, jsonify
import cv2
import time
import threading
from camera import Camera
from detector import Detector
from utils.visualization import draw_detections, draw_fps

app = Flask(__name__)

# Initialize global camera and detector
camera = Camera(0)
detector = Detector()

# Shared state
current_detections = []
latest_frame = None
lock = threading.Lock()

def detection_loop():
    """
    Background thread for continuous object detection.
    """
    global current_detections, latest_frame
    while True:
        ret, frame = camera.get_frame()
        if not ret or frame is None:
            time.sleep(0.01)
            continue
            
        # Perform detection on the latest available frame
        results = detector.detect(frame)
        detections = detector.get_detections(results)
        
        with lock:
            current_detections = detections
            latest_frame = frame.copy()

# Start detection thread
det_thread = threading.Thread(target=detection_loop)
det_thread.daemon = True
det_thread.start()

def generate_frames():
    """
    Efficient frame generation for MJPEG streaming.
    """
    prev_time = time.time()
    
    while True:
        ret, frame = camera.get_frame()
        if not ret or frame is None:
            time.sleep(0.01)
            continue
            
        with lock:
            detections = current_detections.copy()
        
        # Draw detections (on a copy or the original depending on thread safety)
        annotated_frame = draw_detections(frame.copy(), detections)
        
        # FPS calculation
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time)
        prev_time = curr_time
        annotated_frame = draw_fps(annotated_frame, fps)
        
        # Encode as JPEG
        ret, buffer = cv2.imencode('.jpg', annotated_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
        frame_bytes = buffer.tobytes()
        
        # Yield as MJPEG
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), 
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/detections')
def get_detections():
    with lock:
        return jsonify({"detections": current_detections})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
