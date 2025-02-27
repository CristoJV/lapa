# %% Prepare INRIA Dataset's csv

import os
from pathlib import Path
from typing import Any, Dict, List

import cv2
import pandas as pd

from lapa.utils.ops import auto_annotate

dataset_dirpath: Path = Path("/data/inria")
train_dirpath: Path = dataset_dirpath / "train"
test_dirpath: Path = dataset_dirpath / "test"
det_model_filepath: Path = Path("/data/yolo/yolo11x.pt")

# %% Auto-annotate train and test samples
auto_annotate(
    data=train_dirpath / "samples",
    det_model=det_model_filepath,
    device="cuda",
    classes=[0],
    output_dir=train_dirpath / "labels",
)
# Autoanotate test samples
auto_annotate(
    data=test_dirpath / "samples",
    det_model=det_model_filepath,
    device="cuda",
    classes=[0],
    output_dir=test_dirpath / "labels",
)

# %% Prepare and save CSV

data: List[Dict[str, Any]] = []

dirpaths = {"train": train_dirpath, "test": test_dirpath}

for stage, dirpath in dirpaths.items():
    for filepath in os.listdir(dirpath / "samples"):
        sample_id = filepath.split(".")[0]
        sample_filepath = dirpath / "samples" / filepath
        labels_filepath = dirpath / "labels" / f"{sample_id}.txt"
        if labels_filepath.exists():
            image = cv2.imread(sample_filepath)
            img_h, img_w = image.shape[:2]
            for line in labels_filepath.open():
                line = line.split()
                class_id = int(line[0])
                x, y, w, h = map(float, line[1:5])
                data_item = {
                    "sample_id": f"{stage}_{sample_id}",
                    "sample_filepath": sample_filepath.relative_to(
                        dataset_dirpath
                    ),
                    "class_id": class_id,
                    "x": x / img_w,
                    "y": y / img_h,
                    "w": w / img_w,
                    "h": h / img_h,
                    "stage": stage,
                }
                data.append(data_item)

df = pd.DataFrame(data)

df.to_csv(dataset_dirpath / "samples.csv", index=False)

# %%
