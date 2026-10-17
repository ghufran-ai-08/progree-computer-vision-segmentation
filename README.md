
# Computer Vision Object Detection and Frame-by-Frame Segmentation

**Internship:** Progree AI Internship  
**Task:** Task 4 — Computer Vision Object Detector & Frame-by-Frame Segmenter  
**Language:** Python 3.10+  
**Core library:** OpenCV

## 1. Project Overview

This project implements a frame-by-frame video segmentation pipeline using classical computer vision techniques. It processes video frames, isolates bright foreground regions against a dark background, detects contours, draws bounding boxes, displays region counts and processing speed, and records performance metrics.

The project uses a synthetic video containing moving geometric shapes for reproducible testing.

**Scope:** This implementation performs contour-based segmentation. It does not use a trained YOLO model and does not classify objects into semantic categories such as people, vehicles, or animals.

## 2. Features

- Video input and frame-by-frame processing
- Grayscale conversion and Gaussian blur
- Binary intensity thresholding
- Morphological noise removal
- External contour detection and minimum-area filtering
- Bounding boxes and region-area labels
- Dynamic region-count and processing-FPS overlays
- Processed video export
- Periodic annotated-frame extraction
- CSV-based frame metrics
- Performance summary and visualization plots

## 3. Project Structure

```text
Task 4 — Computer Vision Object Detector & Frame-by-Frame Segmenter/
├── src/
│   ├── pipeline.py
│   ├── generate_video.py
│   ├── analyze_results.py
│   └── inspect_frame.py
├── videos/
│   └── synthetic_shapes.mp4
├── results/
│   ├── processed_video.mp4
│   ├── frame_metrics.csv
│   ├── performance_summary.csv
│   ├── frames/
│   └── figures/
│       ├── processing_time.png
│       ├── regions_per_frame.png
│       └── processing_fps.png
├── docs/
│   └── WHITEPAPER.md
├── requirements.txt
├── README.md
└── .gitignore
```

Generated output files may be absent until the corresponding scripts are executed.

## 4. Requirements

- Python 3.10 or newer
- pip
- OpenCV
- NumPy
- Pandas
- Matplotlib

## 5. Installation

Open a terminal in the project root.

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
python -m pip install -r requirements.txt
```

Verify the environment:

```powershell
python -m pip check
```

## 6. Run the Project

### Step 1: Generate a test video

```powershell
python src\generate_video.py
```

The script generates a synthetic moving-shapes video at:

`videos/synthetic_shapes.mp4`

### Step 2: Process the video

```powershell
python src\pipeline.py videos\synthetic_shapes.mp4
```

Optional parameters:

```powershell
python src\pipeline.py videos\synthetic_shapes.mp4 --min-area 500 --save-every 30
```

- `--min-area`: Minimum contour area retained as a region.
- `--save-every`: Interval between saved sample frames.

### Step 3: Analyze the results

```powershell
python src\analyze_results.py
```

This creates performance plots and an aggregate summary CSV.

### Optional: Inspect thresholding

```powershell
python src\inspect_frame.py
```

This diagnostic script examines a saved frame and writes a threshold image.

## 7. Experimental Results

The synthetic test video has a resolution of 640 × 480 pixels, a nominal frame rate of 20 FPS, and 240 frames.

The latest recorded pipeline run produced the following results:

| Metric | Result |
|---|---:|
| Frames processed | 240 |
| Mean detected regions per frame | 3.9625 |
| Minimum regions in a frame | 3 |
| Maximum regions in a frame | 4 |
| Mean processing time | 1.25 ms |
| Mean per-frame FPS | 940.44 |
| Measured frame-processing throughput | 801.48 FPS |
| Broken Python requirements | None reported |

The CSV analysis reported a mean processing time of approximately 1.248 ms. Small differences between displayed values arise from rounding.

The frame-processing throughput is calculated from total processed frames divided by the sum of measured frame-processing times. It excludes video decoding, output writing, and other pipeline overhead. It should not be interpreted as end-to-end application FPS.

## 8. Output Files

| File | Description |
|---|---|
| `results/processed_video.mp4` | Annotated output video |
| `results/frame_metrics.csv` | Frame-level timing and region measurements |
| `results/performance_summary.csv` | Aggregate performance statistics |
| `results/frames/` | Sample annotated frames |
| `results/figures/processing_time.png` | Processing time by frame |
| `results/figures/regions_per_frame.png` | Region counts by frame |
| `results/figures/processing_fps.png` | Per-frame processing throughput |
| `docs/WHITEPAPER.md` | Technical report |

## 9. Limitations

- Thresholding is calibrated for the controlled synthetic video and may not work equally well with arbitrary footage.
- Contours represent segmented regions, not guaranteed unique objects.
- The system does not perform semantic object classification or object tracking.
- No ground-truth annotations were used to calculate precision, recall, IoU, or mean average precision.
- Processing performance depends on the machine, video content, OpenCV build, and timing method.
- The experiment does not establish performance on real-world video.

## 10. Future Improvements

- Evaluate on real-world videos with varying illumination and backgrounds.
- Compare global and adaptive thresholding.
- Tune segmentation parameters using validation data.
- Evaluate against annotated ground-truth bounding boxes.
- Integrate a pretrained YOLO model for semantic object detection.
- Measure end-to-end throughput and latency.

## 11. Reproducibility

From the project root, run:

```powershell
python src\generate_video.py
python src\pipeline.py videos\synthetic_shapes.mp4
python src\analyze_results.py
```

The scripts regenerate the test video, processed output, frame metrics, and performance plots.

## 12. Conclusion

The project demonstrates a reproducible OpenCV video-segmentation workflow covering preprocessing, thresholding, morphological filtering, contour extraction, visualization, CSV logging, and performance analysis. The synthetic experiment processed all 240 frames and detected an average of approximately four regions per frame.

The findings apply to the controlled test video. Additional real-world testing and ground-truth-based evaluation are necessary before drawing conclusions about general object-detection accuracy.

---

**Project:** Progree AI Internship — Task 4  
**Implementation:** Python and OpenCV
'@ | Set-Content -Encoding utf8 README.md
