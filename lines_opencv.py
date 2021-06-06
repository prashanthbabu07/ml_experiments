# %%
from os import path
import os
import cv2
from pdf2image.pdf2image import convert_from_path
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


# files = convert_pdf_to_images("/Volumes/Sandisk/Consulting/Syncortex/Projects/xtract/sample_files/endorsment/unmarked/1004CSR100142020100052_EQP_CT00.PDF",
#                               "/Volumes/Sandisk/Consulting/Syncortex/Projects/xtract/sample_files/endorsment/temp")

# %%

# (1) read
file_name = "/Volumes/Sandisk/Consulting/Syncortex/Projects/xtract/sample_files/endorsment/temp/page_10_1004CSR100142020100052_EQP_CT00.jpg"
img = cv2.imread(file_name)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# %%

# (2) threshold
th, threshed = cv2.threshold(
    gray, 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

# (3) minAreaRect on the nozeros
pts = cv2.findNonZero(threshed)
ret = cv2.minAreaRect(pts)

(cx, cy), (w, h), ang = ret
if w > h:
    w, h = h, w
    ang += 90

# (4) Find rotated matrix, do rotation
# M = cv2.getRotationMatrix2D((cx, cy), ang, 1.0)
# rotated = cv2.warpAffine(threshed, M, (img.shape[1], img.shape[0]))

# (5) find and draw the upper and lower boundary of each lines
hist = cv2.reduce(threshed, 1, cv2.REDUCE_AVG).reshape(-1)

th = 2
H, W = img.shape[:2]
uppers = [y for y in range(H - 1) if hist[y] <= th and hist[y + 1] > th]
lowers = [y for y in range(H - 1) if hist[y] > th and hist[y + 1] <= th]

rotated = cv2.cvtColor(threshed, cv2.COLOR_GRAY2BGR)
for y in uppers:
    cv2.line(threshed, (0, y), (W, y), (255, 0, 0), 1)
    print((0, y), (W, y))

for y in lowers:
    cv2.line(threshed, (0, y), (W, y), (0, 255, 0), 1)
    print((0, y), (W, y))

temp = "/Volumes/Sandisk/Consulting/Syncortex/Projects/xtract/sample_files/endorsment/temp"
cv2.imwrite(os.path.join(temp, "result.png"), threshed)

# %%
