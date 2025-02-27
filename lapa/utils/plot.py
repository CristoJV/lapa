import cv2
import numpy as np

from typing import Dict, List, Literal, Optional, Tuple

from lapa.utils.ops import xywh2xyxy


def draw_bounding_boxes(
    image: np.ndarray,
    bboxes: List[Tuple[float, float, float, float]],
    labels: List[int],  # List of class indices
    bbox_format: Literal["xyxy", "xywh"] = "xyxy",  # "xyxy" or "xywh"
    reference: Literal["center", "topleft"] = "center",
    relative_coords: bool = False,
    scores: Optional[List[float]] = None,  # Confidence scores (optional)
    id2label: Optional[
        Dict[int, str]
    ] = None,  # Mapping from class ID to label
    colormap: Optional[
        Dict[str, Tuple[int, int, int]]
    ] = None,  # Custom colors per class
    default_color: Tuple[int, int, int] = (
        0,
        255,
        0,
    ),  # Default bounding box color
    thickness: int = 2,  # Line thickness for bounding box
    show_label: bool = True,  # Whether to display labels
    font_scale: float = 0.5,  # Font size for labels
    font_thickness: int = 1,  # Font thickness for labels
) -> np.ndarray:
    """
    Draws bounding boxes with labels and optional confidence scores on an image.

    Args:
        image: The input image (H, W, C).
        bboxes: List of bounding boxes.
        labels: List of class indices corresponding to each bounding box.
        bbox_format: Format of bounding boxes, either "xyxy" (xmin, ymin, xmax, ymax) or "xywh" (x, y, width, height).
        normalized_coords: If True, bounding box coordinates are in the range [0, 1] and should be converted to pixels.
        scores: List of confidence scores (optional).
        id2label: Mapping from class ID to label names.
        colormap: Mapping from label to RGB color.
        default_color: Default color for bounding boxes.
        thickness: Thickness of bounding box lines.
        show_label: Whether to display labels on the image.
        font_scale: Font scale for labels.
        font_thickness: Font thickness for labels.

    Returns:
        np.ndarray: Image with bounding boxes drawn.
    """
    annotated_image = image.copy()
    height, width = image.shape[:2]  # Image dimensions

    for i, bbox in enumerate(bboxes):
        if bbox_format == "xyxy":
            xmin, ymin, xmax, ymax = bbox
        elif bbox_format == "xywh":
            bbox = xywh2xyxy(bbox)
            xmin, ymin, xmax, ymax = bbox
            if reference == "center":
                xmin = xmin - bbox[2] / 2
                ymin = ymin - bbox[3] / 2
                xmax = xmax + bbox[2] / 2
                ymax = ymax + bbox[3] / 2
        else:
            raise ValueError("Invalid bbox_format. Choose 'xyxy' or 'xywh'")
        label_id = labels[i]  # Get the class ID

        # Convert normalized coordinates to pixel values if needed
        if relative_coords:
            xmin, xmax = int(xmin * width), int(xmax * width)
            ymin, ymax = int(ymin * height), int(ymax * height)
        else:
            xmin, ymin, xmax, ymax = map(int, [xmin, ymin, xmax, ymax])
        # Get label name if mapping exists
        label_text = (
            id2label[label_id]
            if id2label and label_id in id2label
            else f"Class {label_id}"
        )

        # Get bounding box color from colormap or use default
        color = (
            colormap[label_text]
            if colormap and label_text in colormap
            else default_color
        )

        # Draw bounding box
        cv2.rectangle(
            annotated_image, (xmin, ymin), (xmax, ymax), color, thickness
        )

        # Prepare label text
        if show_label:
            text = label_text
            if scores is not None and i < len(
                scores
            ):  # Add confidence score if available
                text += f" {scores[i]:.2f}"

            # Get text size
            text_size, _ = cv2.getTextSize(
                text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness
            )
            text_width, text_height = text_size

            # Draw background rectangle for text
            cv2.rectangle(
                annotated_image,
                (xmin, ymin - text_height - 4),
                (xmin + text_width + 2, ymin),
                color,
                -1,  # Filled rectangle
            )

            # Draw text
            cv2.putText(
                annotated_image,
                text,
                (xmin, ymin - 4),
                cv2.FONT_HERSHEY_SIMPLEX,
                font_scale,
                (255, 255, 255),  # White text
                font_thickness,
                lineType=cv2.LINE_AA,
            )

    return annotated_image
