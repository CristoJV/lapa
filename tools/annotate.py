# %% Annotate INRIA Dataset


from lapa.utils.ops import auto_annotate


auto_annotate(
    data="/data/inria/train/samples",
    det_model="/data/yolo/yolo11x.pt",
    device="cuda",
    classes=[0],
    output_dir="/data/inria/train/labels",
)
