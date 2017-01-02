import numpy as np
import cv2

class grabCut:
    def __init__(self, image_path):
        self.img = cv2.imread(image_path)

    def simple_cut(self):
        if not isinstance(self.img, np.ndarray):
            raise ValueError("image data is error.")
        img = self.img.copy()
        mask = np.zeros(img.shape[:2], np.uint8)
        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)
        rect = (1, 1, img.shape[0], img.shape[1])
        cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
        img = img * mask2[:, :, np.newaxis]
        return img

    def simple_mask(self):
        img = self.simple_cut()
        for i in np.arange(img.shape[0]):
            for j in np.arange(img.shape[1]):
                if np.all(img[i, j] == [0, 0, 0]):
                    img[i, j] = [255, 255, 255]
        (r, g, b) = cv2.split(img)
        img = cv2.merge([b, g, r])
        return img

    def show(self):
        cv2.imshow(self.img)
        cv2.waitKey()
