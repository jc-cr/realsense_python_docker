import pyrealsense2 as rs
import numpy as np
import cv2
import time
import os

def main():
    print("Starting RealSense camera...")
    pipeline = None
    out = None
    output_path = ""
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
        print(f"Attempting to create VideoWriter for: {output_path}")
        out = cv2.VideoWriter(output_path, 
                              cv2.VideoWriter_fourcc(*'avc1'), 30, (640, 480))
        
        if not out.isOpened():
            raise Exception("Failed to open VideoWriter")

        print(f"VideoWriter created successfully. Recording to {output_path}")
        print("Press 'q' to stop recording...")

        frame_count = 0
        while True:
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
            frame_count += 1

            # Display the frame
            cv2.imshow('RealSense', color_image)
            
            # Check for 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("'q' pressed. Stopping recording...")
                break

    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("Cleaning up...")
        if pipeline:
            pipeline.stop()
        if out:
            out.release()
        cv2.destroyAllWindows()

    print(f"Recording finished. Frames recorded: {frame_count}")
    if os.path.exists(output_path):
        print(f"Output video saved to: {os.path.abspath(output_path)}")
        print(f"File size: {os.path.getsize(output_path)} bytes")
    else:
        print(f"No output file was created or the file is missing at: {output_path}")
        print("Current working directory:", os.getcwd())
        print("Files in current directory:", os.listdir())

if __name__ == "__main__":
    main()
