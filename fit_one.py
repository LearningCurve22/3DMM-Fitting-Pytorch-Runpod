import argparse
import os
import cv2
from util.load_mats import load_BFM
from util.preprocess import align_img
from util.write import write_obj
from core import fit


def main(args):
    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    # Load image
    img = cv2.imread(args.image)
    if img is None:
        raise ValueError(f"Could not read image {args.image}")

    # Preprocess face
    input_img, lm = align_img(img)

    # Load model
    model = load_BFM(args.morphable, args.exp)

    # Run fitting
    fitted_vertices, fitted_colors, fitted_faces = fit(input_img, lm, model)

    # Save as OBJ
    write_obj(args.output, fitted_vertices, fitted_faces, fitted_colors)
    print(f"[OK] Saved 3D face to {args.output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", type=str, required=True)
    parser.add_argument("--morphable", type=str, required=True)
    parser.add_argument("--exp", type=str, required=True)
    parser.add_argument("--output", type=str, default="output.obj")
    args = parser.parse_args()

    main(args)
