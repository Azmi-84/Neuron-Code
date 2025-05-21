import marimo

__generated_with = "0.13.10"
app = marimo.App(width="full")


@app.cell
def __imports():
    import cv2
    import numpy as np
    import time
    from ultralytics import YOLO
    return YOLO, cv2, np, time


@app.cell
def __load_model(YOLO):
    # Load the smallest YOLO model for better performance on CPU
    model = YOLO("yolov8n.pt")
    model.to("cpu")
    return (model,)


@app.cell
def __define_detection_function(cv2, model, np, time):
    def detect_green_circles(frame):
        """Function to detect green circles in a frame"""
        start_time = time.time()
        
        # Resize frame to speed up processing (adjust resolution based on performance)
        frame_resized = cv2.resize(frame, (640, 480))
        
        # Run YOLO detection with CPU optimization
        results = model(frame_resized, verbose=False)
        
        # Post-process to find green objects
        detections = []
        
        # Convert frame to HSV for better color filtering
        hsv = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2HSV)
        
        # Define green color range in HSV
        lower_green = np.array([40, 40, 40])
        upper_green = np.array([80, 255, 255])
        
        # Create mask for green pixels
        green_mask = cv2.inRange(hsv, lower_green, upper_green)
        
        # Scale factor to map back to original frame
        scale_x = frame.shape[1] / frame_resized.shape[1]
        scale_y = frame.shape[0] / frame_resized.shape[0]
        
        for r in results:
            boxes = r.boxes
            for box in boxes:
                # Get box coordinates
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                
                # Check if the detected object is roundish and green
                # Make sure coordinates are within bounds
                if y1 >= frame_resized.shape[0] or y2 >= frame_resized.shape[0] or x1 >= frame_resized.shape[1] or x2 >= frame_resized.shape[1]:
                    continue
                
                # Make sure we have a valid region
                if x2 <= x1 or y2 <= y1:
                    continue
                    
                roi = green_mask[y1:y2, x1:x2]
                if roi.size == 0:  # Skip if ROI is empty
                    continue
                    
                green_percentage = np.sum(roi > 0) / (roi.shape[0] * roi.shape[1])
                
                # Calculate aspect ratio to check if object is circular
                width, height = x2 - x1, y2 - y1
                aspect_ratio = width / height if height > 0 else 0
                
                # If the object is both green and approximately circular
                if green_percentage > 0.5 and 0.8 < aspect_ratio < 1.2:
                    conf = float(box.conf)
                    cls = int(box.cls)
                    name = model.names[cls]
                    
                    # Map coordinates back to original frame
                    orig_x1 = int(x1 * scale_x)
                    orig_y1 = int(y1 * scale_y)
                    orig_x2 = int(x2 * scale_x)
                    orig_y2 = int(y2 * scale_y)
                    
                    detections.append({
                        'bbox': [orig_x1, orig_y1, orig_x2, orig_y2],
                        'confidence': conf,
                        'class': name,
                        'green_percentage': green_percentage
                    })
        
        # Calculate processing time
        process_time = time.time() - start_time
        fps = 1 / process_time if process_time > 0 else 0
        
        return detections, process_time, fps
    
    # Initialize model with a dummy frame for faster first detection
    dummy_frame = np.zeros((640, 640, 3), dtype=np.uint8)
    start_time = time.time()
    _ = model(dummy_frame, verbose=False)
    print(f"Model loaded in {time.time() - start_time:.2f} seconds")
    
    return detect_green_circles


@app.cell
def __process_video(cv2, detect_green_circles, np, time):
    # Define parameters
    source = 0  # 0 for webcam, or provide video file path
    display = True
    
    # Initialize video capture
    cap = cv2.VideoCapture(source)
    
    # Lower the resolution for better performance
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
    
    # Performance tracking variables
    frame_times = []
    total_frames = 0
    skip_frames = 2  # Process every nth frame to improve overall FPS
    
    # Check if camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open video source")
        return None
    
    # Create a UI element to display results
    video_output = marimo.ui.image()
    performance_text = marimo.ui.text("")
    
    # Main processing loop
    def process_frame():
        nonlocal total_frames, frame_times
        
        ret, frame = cap.read()
        if not ret:
            return None
            
        # Process only every nth frame to improve overall FPS
        if total_frames % skip_frames == 0:
            detections, process_time, fps = detect_green_circles(frame)
            frame_times.append(process_time)
            
            # Draw bounding boxes for green circles
            for det in detections:
                x1, y1, x2, y2 = det["bbox"]
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(
                    frame,
                    f"Conf: {det['confidence']:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2,
                )
            
            # Display performance metrics on frame
            avg_time = (
                sum(frame_times[-30:]) / len(frame_times[-30:])
                if frame_times
                else 0
            )
            avg_fps = 1 / avg_time if avg_time > 0 else 0
            
            cv2.putText(
                frame,
                f"FPS: {avg_fps:.1f}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2,
            )
            cv2.putText(
                frame,
                f"Process: {process_time * 1000:.0f}ms",
                (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2,
            )
            
            # Convert frame to RGB for displaying in marimo
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Update the UI elements
            video_output.value = frame_rgb
            
            # Update performance text
            performance_text.value = f"""
            FPS: {avg_fps:.1f}  
            Process time: {process_time * 1000:.0f}ms  
            Total frames: {total_frames}  
            """
        
        total_frames += 1
        return frame
    
    # Create buttons for control
    start_button = marimo.ui.button("Start Detection")
    stop_button = marimo.ui.button("Stop Detection")
    
    # State variables
    running = False
    
    # Define control functions
    def start_detection():
        nonlocal running
        running = True
        # Reset stats
        nonlocal total_frames, frame_times
        total_frames = 0
        frame_times = []
        
        # Processing loop
        while running:
            frame = process_frame()
            if frame is None:
                break
            time.sleep(0.01)  # Small delay to prevent UI freezing
    
    def stop_detection():
        nonlocal running
        running = False
        # Show stats
        if frame_times:
            avg_time = sum(frame_times) / len(frame_times)
            avg_fps = 1 / avg_time if avg_time > 0 else 0
            
            performance_text.value = f"""
            **Performance Summary:**
            Total frames processed: {len(frame_times)}
            Average processing time: {avg_time * 1000:.2f}ms per frame
            Average FPS: {avg_fps:.2f}
            Actual FPS with frame skipping: {avg_fps * (1 / skip_frames):.2f}
            """
    
    # Connect buttons to functions
    start_button.on_click(start_detection)
    stop_button.on_click(stop_detection)
    
    # Create UI layout
    ui = marimo.ui.hstack([
        marimo.ui.vstack([
            start_button,
            stop_button,
            performance_text
        ]),
        video_output
    ])
    
    return ui


@app.cell
def __display_ui(__process_video):
    __process_video
    

@app.cell
def __cleanup(cv2):
    # Make sure to release video capture when app is closed
    def cleanup_resources():
        cv2.destroyAllWindows()
    
    # Register cleanup
    import atexit
    atexit.register(cleanup_resources)
    
    return "YOLO Green Circle Detector ready!"


if __name__ == "__main__":
    app.run()