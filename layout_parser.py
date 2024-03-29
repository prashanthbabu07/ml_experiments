# %%
import layoutparser as lp
from pdf2image import convert_from_path
import os
from os import path
import cv2

# %%


def convert_pdf_to_images(pdf_path, output_path):
    if not path.isfile(pdf_path):
        raise FileNotFoundError()

    if not path.isdir(output_path):
        raise NotADirectoryError()

    name = path.splitext(path.basename(pdf_path))[0]
    pages = convert_from_path(pdf_path, 200)
    image_counter = 1
    image_files = []
    for page in pages:
        filename = os.path.join(output_path, "page_" +
                                str(image_counter) + "_" + name + ".jpg")
        page.save(filename, 'JPEG')
        image_files.append(filename)
        image_counter = image_counter + 1

    return image_files


# %%
convert_pdf_to_images("/Volumes/Sandisk/Consulting/Syncortex/Projects/xtract/sample_files/endorsment/unmarked/1010CSR1202009112335479011_BOP_CT00.PDF",
                      "/Volumes/Sandisk/Consulting/Syncortex/Projects/xtract/sample_files/endorsment/temp")

# %%

# model = lp.Detectron2LayoutModel(
#     'lp://HJDataset/faster_rcnn_R_50_FPN_3x/config',
#     label_map={1: "Title Region", 2: "Text Region", 3: "Title", 4: "Subtitle"})

# model = lp.Detectron2LayoutModel('lp://PubLayNet/faster_rcnn_R_50_FPN_3x/config',
#                                  extra_config=[
#                                      "MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.8],
#                                  label_map={0: "Text", 1: "Title", 2: "List", 3: "Table", 4: "Figure"})


# model = lp.Detectron2LayoutModel('lp://PubLayNet/faster_rcnn_R_50_FPN_3x/config',
#                                  extra_config=[
#                                      "MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.7],
#                                  label_map={0: "Text", 1: "Title", 2: "List", 3: "Table", 4: "Figure"})

# model = lp.Detectron2LayoutModel('lp://PubLayNet/faster_rcnn_R_50_FPN_3x/config',
#                                  extra_config=[
#                                      "MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.7],
#                                  label_map={3: "Table"})

# model = lp.Detectron2LayoutModel("lp://HJDataset/mask_rcnn_R_50_FPN_3x/config",
#                                  label_map={1: "Page Frame", 2: "Row", 3: "Title Region", 4: "Text Region", 5: "Title", 6: "Subtitle", 7: "Other"})

# model = lp.Detectron2LayoutModel(
#     config_path='lp://PubLayNet/mask_rcnn_X_101_32x8d_FPN_3x/config',  # In model catalog
#     label_map={0: "Text", 1: "Title", 2: "List",
#                3: "Table", 4: "Figure"},  # In model`label_map`
#     extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.5]  # Optional
# )

model = lp.Detectron2LayoutModel(
            config_path='p://PrimaLayout/mask_rcnn_R_50_FPN_3x/config',  # In model catalog
            label_map={0: "Text", 1: "Title", 2: "List",
                3: "Table", 4: "Figure"},  # In model`label_map`
            extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.8]  # Optional
# %%
image=cv2.imread(
    "/Volumes/Sandisk/Consulting/Syncortex/Projects/xtract/sample_files/endorsment/temp/page_7_1068csr121302021022130_AUT_App.jpg")

image=image[..., ::-1]

# thresh, img_bin = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)
# %%
# img_bin = 255 - img_bin

# %%
layout=model.detect(image)

# %%
color_map={
    'Text': 'blue',
    'Title': 'red',
    'List': 'green',
    'Table': 'purple',
    'Figure': 'pink',
}
lp.draw_box(image, layout, box_width=3, color_map=color_map)
# %%

text_blocks=lp.Layout([b for b in layout if b.type == 'Title'])

# %%

h, w=image.shape[:2]
# %%

left_interval=lp.Interval(0, w / 2 * 1.05, axis='x').put_on_canvas(image)

left_blocks=text_blocks.filter_by(left_interval, center=True)
left_blocks.sort(key=lambda b: b.coordinates[1])

right_blocks=[b for b in text_blocks if b not in left_blocks]
right_blocks.sort(key=lambda b: b.coordinates[1])

# And finally combine the two list and add the index
# according to the order
text_blocks=lp.Layout([b.set(id=idx)
                         for idx, b in enumerate(left_blocks + right_blocks)])

# %%

lp.draw_box(image, text_blocks,
            box_width=3,
            show_element_id=True)

lp.draw

# %%
