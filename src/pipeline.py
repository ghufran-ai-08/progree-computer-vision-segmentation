
"""Video segmentation pipeline using OpenCV."""

import time
from pathlib import Path

import cv2
import pandas as pd


def process_video(
    input_path,
    output_path="results/processed_video.mp4",
    metrics_path="results/frame_metrics.csv",
    frames_dir="results/frames",
    min_area=500,
    save_every=30,
):
    input_path = Path(input_path)
    output_path = Path(output_path)
    metrics_path = Path(metrics_path)
    frames_dir = Path(frames_dir)

    if not input_path.exists():
        raise FileNotFoundError(f"Input video not found: {input_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    frames_dir.mkdir(parents=True, exist_ok=True)

    cap = cv2.VideoCapture(str(input_path))

    if not cap.isOpened():
        raise RuntimeError(f"Could not open video: {input_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if width <= 0 or height <= 0:
        cap.release()
        raise RuntimeError("Video has invalid dimensions.")

    if fps <= 0:
        fps = 25.0

    writer = cv2.VideoWriter(
        str(output_path),
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height),
    )

    if not writer.isOpened():
        cap.release()
        raise RuntimeError(
            "Could not create output video. Check MP4 codec support."
        )

    metrics = []
    frame_index = 0

    try:
        while True:
            ok, frame = cap.read()

            if not ok:
                break

            start_time = time.perf_counter()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Reduce high-frequency noise before thresholding.
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)

            # Adaptive threshold helps with uneven illumination.
            
            # Segment bright foreground objects against the dark background.
            # Global thresholding is suitable for this controlled synthetic video.
            _, threshold = cv2.threshold(
                blurred,
                80,
                255,
                cv2.THRESH_BINARY,
            )

            # Remove small noise without excessively shrinking the objects.
            kernel = cv2.getStructuringElement(
                cv2.MORPH_ELLIPSE, (3, 3)
            )
            cleaned = cv2.morphologyEx(
                threshold,
                cv2.MORPH_OPEN,
                kernel,
                iterations=1,
            )

            # Retrieve separate external object contours.
            contours, _ = cv2.findContours(
                cleaned,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE,
            )

            detections = []

            for contour in contours:
                area = cv2.contourArea(contour)

                if area < min_area:
                    continue

                x, y, w, h = cv2.boundingRect(contour)
                detections.append((x, y, w, h, area))

                cv2.rectangle(
                    frame, (x, y), (x + w, y + h),
                    (0, 255, 0), 2
                )

                cv2.putText(
                    frame,
                    f"Region {len(detections)}: {int(area)} px",
                    (x, max(y - 8, 20)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    1,
                    cv2.LINE_AA,
                )

            elapsed_ms = (
                time.perf_counter() - start_time
            ) * 1000

            processing_fps = (
                1000 / elapsed_ms if elapsed_ms > 0 else 0
            )

            cv2.putText(
                frame,
                f"Regions: {len(detections)}",
                (15, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2,
            )

            cv2.putText(
                frame,
                f"Processing: {processing_fps:.1f} FPS",
                (15, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2,
            )

            writer.write(frame)

            if frame_index % save_every == 0:
                cv2.imwrite(
                    str(frames_dir / f"frame_{frame_index:06d}.jpg"),
                    frame,
                )

            metrics.append({
                "frame_index": frame_index,
                "timestamp_seconds": frame_index / fps,
                "regions_detected": len(detections),
                "processing_time_ms": elapsed_ms,
                "processing_fps": processing_fps,
                "total_contour_area": sum(
                    item[4] for item in detections
                ),
                "frame_width": width,
                "frame_height": height,
            })

            frame_index += 1

    finally:
        cap.release()
        writer.release()

    if not metrics:
        raise RuntimeError("No frames could be read from the video.")

    df = pd.DataFrame(metrics)
    df.to_csv(metrics_path, index=False)

    
    mean_ms = df["processing_time_ms"].mean()
    mean_frame_fps = df["processing_fps"].mean()
    total_processing_seconds = df["processing_time_ms"].sum() / 1000

    overall_fps = (
        len(df) / total_processing_seconds
        if total_processing_seconds > 0
        else 0
    )

    print(f"Input frames reported by video: {total_frames}")
    print(f"Frames processed: {len(df)}")
    print(f"Average processing time: {mean_ms:.2f} ms")
    print(f"Mean per-frame FPS: {mean_frame_fps:.2f}")
    print(f"Overall measured processing throughput: {overall_fps:.2f} FPS")
    print(f"Average regions per frame: {df['regions_detected'].mean():.2f}")
    print(f"Maximum regions in one frame: {df['regions_detected'].max()}")
    print(f"Minimum regions in one frame: {df['regions_detected'].min()}")
    print(f"Processed video: {output_path.resolve()}")
    print(f"Frame metrics: {metrics_path.resolve()}")

    return df


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Segment contour regions in a video."
    )
    parser.add_argument("video", help="Path to the input video")
    parser.add_argument("--min-area", type=float, default=500)
    parser.add_argument("--save-every", type=int, default=30)
    args = parser.parse_args()

    process_video(
        args.video,
        min_area=args.min_area,
        save_every=args.save_every,
    )
