import pandas as pd
import numpy as np
from PIL import Image
from ultralytics.utils.plotting import Annotator, colors

def add_bboxs_on_img(image: Image, predict: pd.DataFrame):
        annotator = Annotator(np.array(image))

        predict = predict.sort_values(by=['xmin'], ascending=True)

        for index, row in predict.iterrows():
            text = f"{row['name']}: {int(row['confidence']*100)}%"
            bbox = [row['xmin'], row['ymin'], row['xmax'], row['ymax']]
            annotator.box_label(bbox, text, color=colors(row['class'], True))
        return Image.fromarray(annotator.result())