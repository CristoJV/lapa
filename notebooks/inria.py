# %% Visualize INRIA Dataset

import os
from pathlib import Path

import cv2
from matplotlib import pyplot as plt
import torch

from lapa.utils.plot import draw_bounding_boxes

try:
    get_ipython = globals().get(
        "get_ipython", None
    )  # Check if in an IPython environment
    if get_ipython:
        get_ipython().run_line_magic("load_ext", "autoreload")
        get_ipython().run_line_magic("autoreload", "2")
except Exception:
    # Fallback for non-interactive environments
    pass


image_dir = Path("/data/inria/train/samples")
label_dir = Path("/data/inria/train/labels")

number_of_samples = 10

for image_file in os.listdir(image_dir)[:number_of_samples]:
    image_id = image_file.split(".")[0]
    labels_path = label_dir / f"{image_id}.txt"
    if labels_path.exists():
        bboxes = []
        labels = []
        for line in labels_path.open():
            line = line.split()
            class_id = int(line[0])
            x, y, w, h = map(float, line[1:5])
            bboxes.append(torch.Tensor([x, y, w, h]))
            labels.append(class_id)
        image = cv2.imread(str(image_dir / image_file))
        image = image[:, :, ::-1]
        image = draw_bounding_boxes(
            bbox_format="xyxy",
            reference="center",
            relative_coords=False,
            image=image,
            bboxes=bboxes,
            labels=labels,
        )
        plt.imshow(image)
        plt.title("Num of bboxes: " + str(len(bboxes)))
        plt.show()

# %%
