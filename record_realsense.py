import cv2
import time
import os

class VideoRecorder():
    def __init__(self, name="output.mp4", camindex=0, fps=30):
        self.open = True
        self.device_index = camindex
        self.fps = fps
        self.fourcc = "mp4v"
        self.frameSize = (640, 480)
        self.video_filename = name
        self.video_cap = cv2.VideoCapture(self.device_index)
        self.video_writer = cv2.VideoWriter_fourcc(*self.fourcc)
        self.video_out = cv2.VideoWriter(self.video_filename, self.video_writer, self.fps, self.frameSize)
        self.frame_counts = 1
        self.start_time = time.time()

    def record(self):
        while self.open:
            ret, video_frame = self.video_cap.read()
            if ret:
                self.video_out.write(video_frame)
                self.frame_counts += 1
                cv2.imshow("Recording...", video_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.stop()
            else:
                break

    def stop(self):
        if self.open:
            self.open = False
            self.video_out.release()
            self.video_cap.release()
            cv2.destroyAllWindows()

    def start(self):
        print("Press 'q' in the video window to stop recording")
        self.record()

if __name__ == '__main__':
    video_recorder = VideoRecorder()
    video_recorder.start()
    
    elapsed_time = time.time() - video_recorder.start_time
    recorded_fps = video_recorder.frame_counts / elapsed_time
    print(f"Recorded {video_recorder.frame_counts} frames in {elapsed_time:.2f} seconds")
    print(f"Effective frame rate: {recorded_fps:.2f} FPS")
    print(f"Video saved as {video_recorder.video_filename}")
