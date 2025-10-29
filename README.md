# 🟥🟩 Green and Red Rectangular Obstacles Detection

**Real-time obstacle detection system for green and red rectangular objects** — designed for use in the **WRO Future Engineers 2023 obstacle challenge** or similar robotics competitions.

This Python script uses **OpenCV** and **multi-threaded webcam streaming** to detect and highlight rectangular red and green obstacles in a live video feed. It can be used to help autonomous robots identify and avoid obstacles on the track.

---

## 🚀 Features

* ✅ **Real-time detection** using OpenCV
* ✅ **Multi-threaded webcam streaming** for faster frame processing
* 🟥 Detects **red rectangular obstacles**
* 🟩 Detects **green rectangular obstacles**
* 🧠 Filters out non-rectangular shapes using area ratio checks
* 📏 Draws centerlines and boundaries for navigation reference
* ⚙️ Easily adjustable HSV color thresholds

---

## 🧩 How It Works

1. The script captures video frames from the webcam in a **separate thread** for smooth performance.
2. Each frame is:

   * Cropped and contrast-enhanced
   * Converted to HSV color space
   * Masked for **red** and **green** color ranges
3. Contours are extracted from the masks.
4. Each contour is checked:

   * If its area exceeds a threshold (to remove noise)
   * If it is approximately rectangular (based on area ratio)
5. Valid rectangles are highlighted:

   * 🟥 Red contours in **red**
   * 🟩 Green contours in **green**
   * A blue line is drawn through their center (for positional tracking)
6. The frame also includes **left** and **right** guide lines dividing the frame into thirds — useful for navigation logic.

---

## 📸 Example Output

When the script runs, it opens a live video feed window called **“Detection”**.
Detected obstacles will be outlined in color, with guide lines overlaid for spatial awareness.

*(Add a screenshot here once you have one, e.g. `![Detection Example](example.png)`)*

---

## ⚙️ Adjustable Parameters

You can tweak the HSV color ranges or rectangle filtering for your environment or lighting conditions:

```python
# Red color thresholds (two ranges to handle hue wrap-around)
upper_red = np.array([180, 255, 255])
lower_red = np.array([159, 50, 70])
upper_red2 = np.array([9, 255, 255])
lower_red2 = np.array([0, 50, 70])

# Green color thresholds
lower_green = np.array([36, 50, 70])
upper_green = np.array([89, 255, 255])
```

And the rectangularity thresholds:

```python
# Rectangle check ratios
is_rectangle(cnt, ratio, Area)
# Example usage:
# - Red rectangles: ratio > 0.8
# - Green rectangles: ratio > 0.8
```

## 🧭 Applications

* WRO Future Engineers 2023 Obstacle Challenge
* Robot navigation and vision testing
* Color-based object detection experiments
* Embedded robotics camera systems
