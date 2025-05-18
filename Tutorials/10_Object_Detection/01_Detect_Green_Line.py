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

    cv2.namedWindow("Circle Tracker")

    prev_x, prev_y = None, None

    prev_cmd = None
    last_cmd_time = time.time()  # Initialize with current time
    cmd_cooldown = 0.5  # seconds

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Failed to grab frame")
            break

        frame = cv2.flip(frame, 1)  # Flip the frame horizontally

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_green = np.array([35, 70, 70])  # Fixed missing '='
        upper_green = np.array([90, 255, 255])

        mask = cv2.inRange(hsv, lower_green, upper_green)

        kernals = np.ones((5, 5), np.uint8)
        mask = cv2.erode(mask, kernals, iterations=1)
        mask = cv2.dilate(mask, kernals, iterations=1)

        contours, _ = cv2.findContours(
            mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )

        cmd = None

        if contours:
            c = max(contours, key=cv2.contourArea)

            if cv2.contourArea(c) > 500:
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                area = cv2.contourArea(c)
                circle_area = np.pi * radius * radius
                if area / circle_area > 0.6:
                    cv2.circle(
                        frame, (int(x), int(y)), int(radius), (0, 255, 0), 2
                    )
                    cv2.line(
                        frame, (center_x, 0), (center_x, height), (255, 0, 0), 1
                    )
                    cv2.line(
                        frame, (0, center_y), (width, center_y), (255, 0, 0), 1
                    )
                    center_dist = np.sqrt(
                        (x - center_x) ** 2 + (y - center_y) ** 2
                    )

                    if prev_x is not None and prev_y is not None:
                        current_time = time.time()
                        if current_time - last_cmd_time > cmd_cooldown:
                            if abs(x - center_x) > abs(y - center_y):
                                if x < center_x - 50:  # Fixed missing space
                                    cmd = "go left"
                                elif x > center_x + 50:
                                    cmd = "go right"
                            else:
                                if y < center_y - 50:
                                    cmd = "go up"
                                elif y > center_y + 50:
                                    cmd = "go down"

                            if cmd is None:
                                if radius > 70:
                                    cmd = "go backward"
                                elif radius < 30 and radius > 10:
                                    cmd = "go forward"

                            if cmd is not None and cmd != prev_cmd:
                                print(f"Command: {cmd}")
                                prev_cmd = cmd
                                last_cmd_time = current_time

                    prev_x, prev_y = x, y

        if prev_cmd:
            cv2.putText(
                frame,
                prev_cmd,
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,  # Changed prev_command to prev_cmd
                1,
                (0, 0, 255),
                2,
                cv2.LINE_AA,
            )

        cv2.imshow("Circle Tracker", frame)
        cv2.imshow("Mask", mask)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Moved these outside the loop
    cap.release()
    cv2.destroyAllWindows()
    return


if __name__ == "__main__":
    app.run()
