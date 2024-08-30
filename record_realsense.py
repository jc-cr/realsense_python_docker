import pyrealsense2 as rs
import numpy as np
import cv2
import time
from datetime import datetime

class RealSenseRecorder():
    def __init__(self, name_prefix="realsense_recording", fps=30):
        self.fps = fps
        self.fourcc = "mp4v"
        self.frameSize = (640, 480)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.video_filename = f"{name_prefix}_{timestamp}.mp4"
        
        # Configure depth and color streams
        self.pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        
        # Start streaming
        self.pipeline.start(config)
        
        self.video_writer = cv2.VideoWriter_fourcc(*self.fourcc)
        self.video_out = cv2.VideoWriter(self.video_filename, self.video_writer, self.fps, self.frameSize)
        self.frame_counts = 1
        self.start_time = time.time()
        self.open = True

    def record(self):
        try:
            while self.open:
                # Wait for a coherent pair of frames: depth and color
                frames = self.pipeline.wait_for_frames()
                color_frame = frames.get_color_frame()
                if not color_frame:
                    continue

                # Convert images to numpy arrays
                color_image = np.asanyarray(color_frame.get_data())
                
                self.video_out.write(color_image)
                self.frame_counts += 1
                cv2.imshow("RealSense Recording... Press 'q' to stop", color_image)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.stop()
        finally:
            self.stop()

    def stop(self):
        if self.open:
            self.open = False
            self.video_out.release()
            self.pipeline.stop()
            cv2.destroyAllWindows()

    def start(self):
        print(f"Recording started. Output file: {self.video_filename}")
        print("Press 'q' in the video window to stop recording")
        self.record()

if __name__ == '__main__':
    recorder = RealSenseRecorder()
    recorder.start()
    
    elapsed_time = time.time() - recorder.start_time
    recorded_fps = recorder.frame_counts / elapsed_time
    print(f"Recorded {recorder.frame_counts} frames in {elapsed_time:.2f} seconds")
    print(f"Effective frame rate: {recorded_fps:.2f} FPS")
    print(f"Video saved as {recorder.video_filename}")
