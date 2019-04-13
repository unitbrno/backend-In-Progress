import cv2
import numpy as np
import matplotlib as mpl
import matplotlib.cm as mtpltcm


class Effect:
    """Doc string for Effect"""

    def __init__(self, effect):
        if effect not in self.get_effects():
            raise NameError
        self.effect = effect

    def apply(self, frame):
        if self.effect is None:
            return frame
        elif self.effect == "cartoon":
            return self.cartoon_effect(frame)
        elif self.effect == "wtf":
            return self.wtf(frame)
        elif self.effect == "maximize":
            return self.maximize(frame)
        elif self.effect == "thermal":
            return self.thermal(frame)
        elif self.effect == "red":
            return self.red(frame)
        elif self.effect == "green":
            return self.green(frame)
        elif self.effect == "blue":
            return self.blue(frame)

    @staticmethod
    def cartoon_effect(frame):
        frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.adaptiveThreshold(cv2.medianBlur(frame_bw, 5), 255,
                                      cv2.ADAPTIVE_THRESH_MEAN_C,
                                      cv2.THRESH_BINARY, 9, 9)
        color = cv2.bilateralFilter(frame, 9, 300, 300)
        return cv2.bitwise_and(color, color, mask=edges)

    @staticmethod
    def wtf(frame):
        # https://people.revoledu.com/kardi/tutorial/Python/Video+Analysis+using+OpenCV-Python.html
        # equalize the histogram of color image
        img = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)  # convert to HSV
        # equalize the histogram of the V channel
        img[:, :, 2] = cv2.equalizeHist(img[:, :, 2])
        # convert the HSV image back to RGB format
        return img

    @staticmethod
    def maximize(frame):
        (B, G, R) = cv2.split(frame)
        # find the maximum pixel intensity values for each
        # (x, y)-coordinate,, then set all pixel values less
        # than M to zero
        M = np.maximum(np.maximum(R, G), B)
        R[R < M] = 0
        G[G < M] = 0
        B[B < M] = 0
        # merge the channels back together and return the image
        return cv2.merge([B, G, R])

    @staticmethod
    def thermal(frame):
        # https://blog.bastelhalde.de/post/creating-fake-thermal-images-using-python
        # initialize the colormap (jet)
        colormap = mpl.cm.jet
        # add a normalization
        cNorm = mpl.colors.Normalize(vmin=0, vmax=255)
        # init the mapping
        scalarMap = mtpltcm.ScalarMappable(norm=cNorm, cmap=colormap)
        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # add blur to make it more realistic
        blur = cv2.GaussianBlur(gray, (15, 15), 0)
        # assign colormap and return the image
        return scalarMap.to_rgba(blur, bytes=False)

    @staticmethod
    def red(frame):
        red = frame[:, :, 2]
        img = np.zeros((red.shape[0], red.shape[1], 3), dtype=red.dtype)
        img[:, :, 2] = red
        return img

    @staticmethod
    def green(frame):
        green = frame[:, :, 1]
        img = np.zeros((green.shape[0], green.shape[1], 3), dtype=green.dtype)
        img[:, :, 1] = green
        return img

    @staticmethod
    def blue(frame):
        blue = frame[:, :, 0]
        img = np.zeros((blue.shape[0], blue.shape[1], 3), dtype=blue.dtype)
        img[:, :, 0] = blue
        return img

    @staticmethod
    def get_effects():
        return [
            None,
            # https://pysource.com/2018/10/11/how-to-create-a-cartoon-effect-opencv-with-python/
            "cartoon",
            "wtf",
            "maximize",
            "thermal",
            "red",
            "green",
            "blue",
        ]
