import marimo

__generated_with = "0.13.10"
app = marimo.App(width="full", app_title="Detect Green Line")


@app.cell
def _():
    import cv2
    import numpy as np
    import time
    return cv2, np, time


@app.cell
def _(cv2, np, time):
    cap = cv2.VideoCapture(0)

    width = 640
    height = 480
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    center_x = width // 2
    center_y = height // 2

    cv2.namedWindow("Paper Tracker")

    prev_x, prev_y = None, None

    prev_cmd = None
    last_cmd_time = time.time()
    cmd_cooldown = 0.5  # seconds

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Failed to grab frame")
            break

        frame = cv2.flip(frame, 1)  # Flip the frame horizontally

        # Convert to grayscale to better detect white paper with black markings
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Apply adaptive thresholding to detect white paper
        # The white paper will appear bright in the image
        thresh = cv2.adaptiveThreshold(
            blurred,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            11,
            2,
        )

        # Find contours in the thresholded image
        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        cmd = None

        if contours:
            # Find the largest contour (assuming it's the paper)
            c = max(contours, key=cv2.contourArea)

            if (
                cv2.contourArea(c) > 5000
            ):  # Increased min area since paper is larger
                # Get the bounding rectangle
                x, y, w, h = cv2.boundingRect(c)

                # Calculate center of the paper
                paper_x = x + w // 2
                paper_y = y + h // 2

                # Draw rectangle around paper
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Draw center lines
                cv2.line(frame, (center_x, 0), (center_x, height), (255, 0, 0), 1)
                cv2.line(frame, (0, center_y), (width, center_y), (255, 0, 0), 1)

                # Calculate "radius" as half the diagonal for size estimation
                radius = np.sqrt(w * w + h * h) / 2

                if prev_x is not None and prev_y is not None:
                    current_time = time.time()
                    if current_time - last_cmd_time > cmd_cooldown:
                        if abs(paper_x - center_x) > abs(paper_y - center_y):
                            if paper_x < center_x - 50:
                                cmd = "go left"
                            elif paper_x > center_x + 50:
                                cmd = "go right"
                        else:
                            if paper_y < center_y - 50:
                                cmd = "go up"
                            elif paper_y > center_y + 50:
                                cmd = "go down"

                        if cmd is None:
                            if radius > 200:  # Adjusted for paper size
                                cmd = "go backward"
                            elif radius < 150 and radius > 50:
                                cmd = "go forward"

                        if cmd is not None and cmd != prev_cmd:
                            print(f"Command: {cmd}")
                            prev_cmd = cmd
                            last_cmd_time = current_time

                prev_x, prev_y = paper_x, paper_y

        if prev_cmd:
            cv2.putText(
                frame,
                prev_cmd,
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2,
                cv2.LINE_AA,
            )

        cv2.imshow("Paper Tracker", frame)
        cv2.imshow("Threshold", thresh)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    return


if __name__ == "__main__":
    app.run()
