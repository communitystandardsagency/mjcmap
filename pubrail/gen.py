import os

from PIL import Image
import numpy as np

def extend_to_ratio(img, target_w, target_h):
    src_w, src_h = img.size
    target_width = int(src_h * target_w / target_h)

    if target_width <= src_w:
        print(f"  Warning: target width {target_width}px <= source width {src_w}px, returning original.")
        return img.copy()

    padding = target_width - src_w
    pad_left = padding // 2
    pad_right = padding - pad_left

    img_array = np.array(img)

    left_col = img_array[:, 0:1, :]   # shape (H, 1, C)
    right_col = img_array[:, -1:, :]  # shape (H, 1, C)

    left_fill = np.repeat(left_col, pad_left, axis=1)
    right_fill = np.repeat(right_col, pad_right, axis=1)

    extended = np.concatenate([left_fill, img_array, right_fill], axis=1)
    return Image.fromarray(extended)


def main():
    source_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "full.png")
    print(f"Loading '{source_path}'...")
    img = Image.open(source_path).convert("RGBA")
    print(f"  Source size: {img.size[0]}x{img.size[1]}px")

    script_dir = os.path.dirname(os.path.abspath(__file__))

    outputs = [
    (os.path.join(script_dir, "tv.png"),     32, 19),
    (os.path.join(script_dir, "big_tv.png"), 42, 28),
    #(os.path.join(script_dir, "box_tv.png"), 12,  8),
    ]

    for filename, rw, rh in outputs:
        print(f"\nGenerating '{filename}' (ratio {rw}:{rh})...")
        result = extend_to_ratio(img, rw, rh)
        result.save(filename)
        print(f"  Saved: {result.size[0]}x{result.size[1]}px → '{filename}'")

    print("\nDone.")


if __name__ == "__main__":
    main()
