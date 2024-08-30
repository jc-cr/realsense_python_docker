import pyrealsense2 as rs
import numpy as np
import cv2
import time
import signal
import sys
import os

# Global variables
recording = True
output_path = ""

def signal_handler(sig, frame):
    global recording
    print("Stopping recording...")
    recording = False

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)

def main():
    global output_path
    print("Starting RealSense camera...")
    try:
        # Configure depth and color streams
        pipeline = rs.pipeline()
        config = rs.config()

        # Get device product line for setting a supporting resolution
        pipeline_wrapper = rs.pipeline_wrapper(pipeline)
        pipeline_profile = config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()
        device_product_line = str(device.get_info(rs.camera_info.product_line))
        print(f"Found device: {device_product_line}")

        # Configure the pipeline to stream the color sensor
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

        # Start streaming
        print("Starting pipeline...")
        pipeline.start(config)

        # Create a VideoWriter object
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        output_path = f'output_{timestamp}.mp4'
        out = cv2.VideoWriter(output_path, 
                              cv2.VideoWriter_fourcc(*'avc1'), 30, (640, 480))

        print(f"Recording to {output_path}")
        print("Press 'q' to stop recording...")

        while recording:
            # Wait for a coherent pair of frames: depth and color
            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            if not color_frame:
                print("No color frame received")
                continue

            # Convert images to numpy arrays
            color_image = np.asanyarray(color_frame.get_data())

            # Write the frame
            out.write(color_image)

            # Display the frame
            cv2.imshow('RealSense', color_image)
            
            # Check for 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("'q' pressed. Stopping recording...")
                break

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Cleaning up...")
        # Stop streaming
        pipeline.stop()
        # Release the VideoWriter
        out.release()
        # Close OpenCV windows
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
    print("Recording finished.")
    if output_path:
        print(f"Output video saved to: {os.path.abspath(output_path)}")
    else:
        print("No output file was created.")
import numpy as np
import cv2
import time
import signal
import sys
import os

# Global flag to control recording
recording = True

def signal_handler(sig, frame):
    global recording
    print("Stopping recording...")
    recording = False

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)

def main():
    print("Starting RealSense camera...")
    try:
        # Configure depth and color streams
        pipeline = rs.pipeline()
        config = rs.config()

        # Get device product line for setting a supporting resolution
        pipeline_wrapper = rs.pipeline_wrapper(pipeline)
        pipeline_profile = config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()
        device_product_line = str(device.get_info(rs.camera_info.product_line))
        print(f"Found device: {device_product_line}")

        # Configure the pipeline to stream the color sensor
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

        # Start streaming
        print("Starting pipeline...")
        pipeline.start(config)

        # Create a VideoWriter object
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        output_path = f'output_{timestamp}.mp4'
        out = cv2.VideoWriter(output_path, 
                              cv2.VideoWriter_fourcc(*'avc1'), 30, (640, 480))

        print(f"Recording to {output_path}")
        print("Press 'q' to stop recording...")

        while recording:
            # Wait for a coherent pair of frames: depth and color
            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            if not color_frame:
                print("No color frame received")
                continue

            # Convert images to numpy arrays
            color_image = np.asanyarray(color_frame.get_data())

            # Write the frame
            out.write(color_image)

            # Display the frame
            cv2.imshow('RealSense', color_image)
            
            # Check for 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("'q' pressed. Stopping recording...")
                break

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Cleaning up...")
        # Stop streaming
        pipeline.stop()
        # Release the VideoWriter
        out.release()
        # Close OpenCV windows
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
    print("Recording finished.")
    print(f"Output video saved to: {os.path.abspath(output_path)}")
