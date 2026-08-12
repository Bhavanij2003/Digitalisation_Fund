"""
calibrate_template.py

A small interactive tool to calibrate field regions against the ACTUAL
blank Suryan Benefit Fund forms, since the coordinates shipped in
backend/templates_config.py are only reasonable placeholders.

Usage:
    python calibrate_template.py <path_to_blank_form_image> <deposit|share>

Instructions shown in the window:
  - The image is resized to the same STANDARD_WIDTH x STANDARD_HEIGHT used
    by preprocessing.py, so the coordinates you calibrate match exactly what
    the OCR pipeline will crop.
  - Click and drag to draw a rectangle over a field.
  - After releasing the mouse you will be asked (in the terminal) to type
    the field name (must match a key in templates_config.py) and press Enter.
  - Press 'q' to finish. A JSON block with correctly scaled fractional
    coordinates will be printed - paste it into templates_config.py.
  - Press 'u' to undo the last box.

This keeps calibration a one-time, five-minute manual step per form type,
which is far more reliable than trying to auto-detect arbitrary form
layouts.
"""

import sys
import os
import json
import cv2

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "backend"))
from preprocessing import STANDARD_WIDTH, STANDARD_HEIGHT  # noqa: E402

drawing = False
ix, iy = -1, -1
boxes = {}  # field_name -> (x, y, w, h) in pixels
current_image = None
display_image = None


def redraw():
    global display_image
    display_image = current_image.copy()
    for name, (x, y, w, h) in boxes.items():
        cv2.rectangle(display_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(display_image, name, (x, max(0, y - 5)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)


def mouse_callback(event, x, y, flags, param):
    global ix, iy, drawing, display_image

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        redraw()
        cv2.rectangle(display_image, (ix, iy), (x, y), (255, 0, 0), 2)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        x0, y0 = min(ix, x), min(iy, y)
        w, h = abs(x - ix), abs(y - iy)
        if w > 3 and h > 3:
            field_name = input("Field name for this box (must match templates_config.py key): ").strip()
            if field_name:
                boxes[field_name] = (x0, y0, w, h)
        redraw()


def main():
    global current_image, display_image

    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    image_path = sys.argv[1]
    form_type = sys.argv[2]

    img = cv2.imread(image_path)
    if img is None:
        print(f"Could not read image: {image_path}")
        sys.exit(1)

    current_image = cv2.resize(img, (STANDARD_WIDTH, STANDARD_HEIGHT))
    redraw()

    window = f"Calibrate: {form_type} (drag to box a field, 'u' undo, 'q' finish)"
    cv2.namedWindow(window, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window, 900, 1150)
    cv2.setMouseCallback(window, mouse_callback)

    while True:
        cv2.imshow(window, display_image)
        key = cv2.waitKey(20) & 0xFF
        if key == ord("q"):
            break
        if key == ord("u") and boxes:
            boxes.pop(list(boxes.keys())[-1])
            redraw()

    cv2.destroyAllWindows()

    print("\n--- Paste this into templates_config.py (as fractional coordinates) ---\n")
    result = {}
    for name, (x, y, w, h) in boxes.items():
        result[name] = {
            "x": round(x / STANDARD_WIDTH, 4),
            "y": round(y / STANDARD_HEIGHT, 4),
            "w": round(w / STANDARD_WIDTH, 4),
            "h": round(h / STANDARD_HEIGHT, 4),
            "type": "text",
        }
    print(json.dumps(result, indent=4))

    out_path = f"calibration_{form_type}.json"
    with open(out_path, "w") as f:
        json.dump(result, f, indent=4)
    print(f"\nAlso saved to {out_path}")


if __name__ == "__main__":
    main()
