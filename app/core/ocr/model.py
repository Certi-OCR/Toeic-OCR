from ultralytics import YOLO
from pathlib import Path

model = YOLO(Path.cwd().joinpath("model", "toeicLR.pt"))
