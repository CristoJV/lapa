from pathlib import Path
import numpy as np
import torch
from ultralytics import YOLO


def xywh2xyxy(x):
    """
    Convert bounding box coordinates from (x, y, width, height) format to (x1, y1, x2, y2) format where (x1, y1) is the
    top-left corner and (x2, y2) is the bottom-right corner. Note: ops per 2 channels faster than per channel.

    Args:
        x (np.ndarray | torch.Tensor): The input bounding box coordinates in (x, y, width, height) format.

    Returns:
        y (np.ndarray | torch.Tensor): The bounding box coordinates in (x1, y1, x2, y2) format.
    """
    assert (
        x.shape[-1] == 4
    ), f"input shape last dimension expected 4 but input shape is {x.shape}"
    y = empty_like(x)  # faster than clone/copy
    xy = x[..., :2]  # centers
    wh = x[..., 2:] / 2  # half width-height
    y[..., :2] = xy - wh  # top left xy
    y[..., 2:] = xy + wh  # bottom right xy
    return y


def empty_like(x):
    """Creates empty torch.Tensor or np.ndarray with same shape as input and float32 dtype."""
    return (
        torch.empty_like(x, dtype=torch.float32)
        if isinstance(x, torch.Tensor)
        else np.empty_like(x, dtype=np.float32)
    )


def auto_annotate(
    data,
    det_model="yolo11x.pt",
    device="",
    conf=0.25,
    iou=0.45,
    imgsz=640,
    max_det=300,
    classes=None,
    output_dir=None,
):
    """
    Automatically annotates images using a YOLO object detection model and a SAM segmentation model.

    This function processes images in a specified directory, detects objects using a YOLO model, and then generates
    segmentation masks using a SAM model. The resulting annotations are saved as text files.

    Args:
        data (str): Path to a folder containing images to be annotated.
        det_model (str): Path or name of the pre-trained YOLO detection model.device (str): Device to run the models on (e.g., 'cpu', 'cuda', '0').
        conf (float): Confidence threshold for detection model; default is 0.25.
        iou (float): IoU threshold for filtering overlapping boxes in detection results; default is 0.45.
        imgsz (int): Input image resize dimension; default is 640.
        max_det (int): Limits detections per image to control outputs in dense scenes.
        classes (list): Filters predictions to specified class IDs, returning only relevant detections.
        output_dir (str | None): Directory to save the annotated results. If None, a default directory is created.

    Examples:
        >>> from ultralytics.data.annotator import auto_annotate
        >>> auto_annotate(data="ultralytics/assets", det_model="yolo11n.pt")

    Notes:
        - The function creates a new directory for output if not specified.
        - Annotation results are saved as text files with the same names as the input images.
        - Each line in the output text file represents a detected object with its class ID and segmentation points.
    """
    det_model = YOLO(det_model)

    data = Path(data)
    if not output_dir:
        output_dir = data.parent / f"{data.stem}_auto_annotate_labels"
    Path(output_dir).mkdir(exist_ok=True, parents=True)

    det_results = det_model(
        data,
        stream=True,
        device=device,
        conf=conf,
        iou=iou,
        imgsz=imgsz,
        max_det=max_det,
        classes=classes,
    )

    for result in det_results:
        class_ids = result.boxes.cls.int().tolist()  # noqa
        if class_ids:
            boxes = result.boxes.xyxy  # Boxes object for bbox outputs
            with open(
                f"{Path(output_dir) / Path(result.path).stem}.txt", "w"
            ) as f:
                for i, box in enumerate(boxes):
                    box = map(str, box.reshape(-1).tolist())
                    f.write(f"{class_ids[i]} " + " ".join(box) + "\n")
