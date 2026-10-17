
import cv2
import numpy as np
from pathlib import Path
import math

OUTPUT = Path("videos/synthetic_shapes.mp4")

WIDTH = 640
HEIGHT = 480
FPS = 20
TOTAL_FRAMES = 240  # 12 seconds


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(
        str(OUTPUT), fourcc, FPS, (WIDTH, HEIGHT)
    )

    if not writer.isOpened():
        raise RuntimeError(
            "Could not create the video. Check OpenCV video codec support."
        )

    for frame_no in range(TOTAL_FRAMES):
        frame = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
        frame[:] = (25, 25, 25)

        t = frame_no / FPS

        # Moving bright circle
        x1 = int(100 + 65 * math.sin(t * 1.2))
        y1 = int(110 + 45 * math.cos(t * 1.5))
        cv2.circle(frame, (x1, y1), 32, (255, 255, 255), -1)

        # Moving rectangle
        x2 = int(320 + 100 * math.sin(t * 0.8))
        y2 = int(240 + 70 * math.cos(t * 1.1))
        cv2.rectangle(
            frame, (x2 - 35, y2 - 25),
            (x2 + 35, y2 + 25), (220, 220, 220), -1
        )

        # Moving triangle
        x3 = int(500 + 55 * math.cos(t))
        y3 = int(120 + 55 * math.sin(t * 1.3))
        triangle = np.array([
            [x3, y3 - 35],
            [x3 - 32, y3 + 25],
            [x3 + 32, y3 + 25]
        ], dtype=np.int32)
        cv2.fillPoly(frame, [triangle], (245, 245, 245))

        # Additional moving circle
        x4 = int(180 + 80 * math.cos(t * 0.9))
        y4 = int(360 + 35 * math.sin(t * 1.4))
        cv2.circle(frame, (x4, y4), 20, (190, 190, 190), -1)

        writer.write(frame)

    writer.release()

    # Verify that the saved video can be reopened.
    cap = cv2.VideoCapture(str(OUTPUT))
    if not cap.isOpened():
        raise RuntimeError("Video was saved but cannot be reopened.")

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()

    print("Synthetic video generated successfully.")
    print(f"File: {OUTPUT.resolve()}")
    print(f"Resolution: {width} x {height}")
    print(f"Frames: {frame_count}")
    print(f"Duration: {frame_count / FPS:.1f} seconds")


if __name__ == "__main__":
    main()
