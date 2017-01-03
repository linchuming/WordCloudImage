import numpy as np
import cv2

class grabCut:
    def __init__(self, image_path):
        self.pre_x = -1
        self.pre_y = -1
        self.cur_x = -1
        self.cur_y = -1
        self.tmp = None
        self.crop_img = None
        self.img = cv2.imread(image_path)
        self.rect = (1, 1, self.img.shape[1], self.img.shape[0])
        self.drawing = False
        self.mask = np.ones(self.img.shape[:2], np.uint8) * cv2.GC_PR_FGD

    def simple_cut(self):
        if not isinstance(self.img, np.ndarray):
            raise ValueError("image data is error.")
        img = self.img.copy()
        mask = np.zeros(img.shape[:2], np.uint8)
        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)
        cv2.grabCut(img, mask, self.rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
        mask2 = np.where((mask == cv2.GC_PR_BGD) | (mask == cv2.GC_BGD), 0, 1).astype('uint8')
        img = img * mask2[:, :, np.newaxis]
        img += 255 * (1 - cv2.cvtColor(mask2, cv2.COLOR_GRAY2BGR))
        r = self.rect
        return img[r[1]-1:r[1]+r[3]-1, r[0]-1:r[0]+r[2]-1]

    def simple_mask(self):
        img = self.simple_cut()
        (r, g, b) = cv2.split(img)
        img = cv2.merge([b, g, r])
        return img

    def hand_cut(self):
        if not isinstance(self.img, np.ndarray):
            raise ValueError("image data is error.")
        img = self.img.copy()
        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)
        cv2.grabCut(img, self.mask, None, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_MASK)
        mask2 = np.where((self.mask == cv2.GC_PR_BGD) | (self.mask == cv2.GC_BGD), 0, 1).astype('uint8')
        img = img * mask2[:, :, np.newaxis]
        img += 255 * (1 - cv2.cvtColor(mask2, cv2.COLOR_GRAY2BGR))
        r = self.rect
        return img[r[1]-1:r[1] + r[3]-1, r[0]-1:r[0] + r[2]-1]

    def hand_mask(self):
        img = self.hand_cut()
        (r, g, b) = cv2.split(img)
        img = cv2.merge([b, g, r])
        return img

    def show(self):
        cv2.imshow('image', self.img)
        cv2.waitKey()

    def set_rect(self):
        cv2.namedWindow('imageCrop')
        cv2.setMouseCallback('imageCrop', self.rect_func)
        self.tmp = self.img.copy()
        cv2.imshow('imageCrop', self.tmp)
        self.drawing = True
        while(self.drawing):
            cv2.waitKey(100)

    def rect_func(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.pre_x = x
            self.pre_y = y

        elif event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_LBUTTON):
            tmp = self.tmp.copy()
            self.cur_x = x
            self.cur_y = y
            cv2.rectangle(tmp, (self.pre_x, self.pre_y), (self.cur_x, self.cur_y),
                          (255, 0, 0), 1, 8, 0)
            cv2.imshow('imageCrop', tmp)

        elif event == cv2.EVENT_LBUTTONUP:
            width = abs(self.cur_x - self.pre_x)
            height = abs(self.cur_y - self.pre_y)
            if width == 0 or height == 0:
                print "crop rect is wrong."
                return
            sx = min(self.pre_x, self.cur_x)
            sy = min(self.pre_y, self.cur_y)
            self.rect = (sx, sy, width, height)
            self.drawing = False

    def hand_label(self):
        self.tmp = self.img.copy()
        self.mask = np.zeros(self.tmp.shape[:2], np.uint8)
        r = self.rect
        self.mask[r[1]-1:r[1]+r[3]-1, r[0]-1:r[0]+r[2]-1] = cv2.GC_PR_FGD
        cv2.namedWindow('handLabel')
        cv2.setMouseCallback('handLabel', self.label_func)
        cv2.imshow('handLabel', self.tmp)
        while (True):
            if cv2.waitKey(20)&0xff == 27:
                break

    def label_func(self, event, x, y, flags, param):
        if event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_LBUTTON):
            cv2.circle(self.tmp, (x, y), 2, (0, 255, 0), -1, cv2.CV_AA)
            self.mask[y-1,x-1] = cv2.GC_FGD
            cv2.imshow('handLabel', self.tmp)
        elif event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_RBUTTON):
            cv2.circle(self.tmp, (x, y), 2, (0, 0, 255), -1, cv2.CV_AA)
            self.mask[y-1,x-1] = cv2.GC_BGD
            cv2.imshow('handLabel', self.tmp)
