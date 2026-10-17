
import cv2
from pathlib import Path

frame_path = Path("results/frames/frame_000060.jpg")

image = cv2.imread(str(frame_path))
if image is None:
    raise FileNotFoundError(f"Could not read {frame_path}")

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

threshold = cv2.adaptiveThreshold(
    blurred,
    255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY,
    21,
    5,
)

contours, _ = cv2.findContours(
    threshold,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE,
)

print(f"Frame dimensions: {image.shape[1]} x {image.shape[0]}")
print(f"Contours before area filtering: {len(contours)}")

for i, contour in enumerate(contours):
    area = cv2.contourArea(contour)
    x, y, w, h = cv2.boundingRect(contour)
    print(
        f"Contour {i + 1}: area={area:.1f}, "
        f"box=({x}, {y}, {w}, {h})"
    )

output_path = Path("results/figures/threshold_diagnostic.png")
output_path.parent.mkdir(parents=True, exist_ok=True)
cv2.imwrite(str(output_path), threshold)

print(f"Threshold image saved to: {output_path.resolve()}")
