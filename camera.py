import cv2
import threading
import time

class Camera:
    def __init__(self, source=0):
        """
        Initialize the camera with a background thread for reading frames.
        :param source: Webcam index or video file path.
        """
        self.cap = cv2.VideoCapture(source)
        if not self.cap.isOpened():
            raise ValueError(f"Unable to open video source {source}")
        
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        
        self.ret = False
        self.frame = None
        self.stopped = False
        
        # Start background thread
        self.thread = threading.Thread(target=self._update, args=())
        self.thread.daemon = True
        self.thread.start()

    def _update(self):
        """
        Continuously read frames from the camera.
        """
        while True:
            if self.stopped:
                return
            self.ret, self.frame = self.cap.read()

    def get_frame(self):
        """
        Return the latest frame captured by the background thread.
        :return: Success flag and the frame.
        """
        return self.ret, self.frame

    def release(self):
        """
        Stop the thread and release camera resources.
        """
        self.stopped = True
        if self.thread.is_alive():
            self.thread.join()
        if self.cap.isOpened():
            self.cap.release()

if __name__ == "__main__":
    # Simple test for camera capture
    cam = Camera(0)
    print(f"Resolution: {cam.width}x{cam.height}, FPS: {cam.fps}")
    while True:
        ret, frame = cam.get_frame()
        if not ret:
            break
        cv2.imshow("Camera Test", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()
