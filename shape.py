import cv2
import numpy as np
from random import randint

class Shape:
    """docstring for Shape"""

    curves = {
        'curve1': [
            # percentages of frame width defining x points
            np.linspace(0, 1, 10),
            # percentages of frame height defining y points
            [0.1, 0.15, 0.25, 0.40, 0.5, 0.65, 0.75, 0.8, 0.85, 0.9],
            # speed diffs at the x points
            [0, 0, 0, 1, 3, 3, 3, 5, 5, 9],
        ],
        'curve2': [
            np.linspace(0, 1, 10),
            [0.1, 0.15, 0.4, 0.6, 0.7, 0.75, 0.7, 0.5, 0.3, 0.1],
            [0, 15, 50, 50, 45, 0, 0, 20, 35, 100],
        ],
        'curve3': [
            np.linspace(0, 1, 10),
            [0.8, 0.75, 0.7, 0.6, 0.4, 0.1, 0.4, 0.6, 0.8, 0.9],
            [0, 0, 0, 1, 3, 3, 3, 5, 5, 9],
        ],
        # it's actually linear (almost 1am) :D
        'curve4': [
            np.linspace(0, 1, 10),
            [0.45] * 10,
            [0] * 10,
        ],
        # it's a fall (almost 1:30am) :D
        # If it's fallin' down, I'm yellin' timber...
        'fall': [
            np.linspace(0, 1, 10),
            [0.5, 0.45, 0.5, 0.45, 0.4, 0.45, 0.5, 0.4, 0.43, 0.5],
            [0] * 10,
        ]
    }

    def __init__(self, width, height, x, y, speed, image, animation):
        self.end = False
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.image = cv2.imread(image, -1) if image else None
        height, width, depth = self.image.shape
        img_scale = 600/width
        new_x = self.image.shape[1]*img_scale
        new_y = self.image.shape[0]*img_scale
        self.image = cv2.resize(self.image, (int(new_x), int(new_y)))
        self.imagegrey = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.speed = speed
        # rows, cols, channels
        self.dim = self.image.shape
        if x < width / 2:
            self.offset = - int(self.dim[1] / 2)
        else:
            self.offset = int(self.dim[1] / 2)
        self.animation = animation
        if animation.startswith("curve"):
            self.animation_func = self.prepare_animation(animation)
        elif animation.startswith("fall"):
            self.animation_func = self.prepare_animation_inverse(animation)

    def paint(self, frame):
        """Paint new position of image into a frame."""
        self._next_pos()
        roi = frame[0: self.dim[0], 0: self.dim[1]]  # noqa: 203
        __, mask = cv2.threshold(self.imagegrey, 10, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        # Now black-out the area of logo in ROI
        frame_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
        # Take only region of logo from logo image.
        image_fg = cv2.bitwise_and(self.image, self.image, mask=mask)
        # Put logo in ROI and modify the main image
        dst = cv2.add(frame_bg, image_fg)

        if (self.x + self.dim[0] > self.height) or \
                (self.y > self.width - self.dim[1]):
            return
        if self.image is not None:
            frame[
                self.x: (self.dim[0] + self.x),  # noqa: 203
                self.y: (self.dim[1] + self.y),  # noqa: 203
            ] = dst

    def _next_pos(self):
        """Get next position and speed from animation functions."""
        if self.animation.startswith("linear"):
            self.x += self.speed
            self.y += self.speed
            if self.x + self.dim[0] > self.height:
                self.x = 0
            if self.y > self.width - self.dim[1]:
                self.y = 0
                self.end = True
        elif self.animation.startswith("fall"):
            if self.x + self.dim[0] >= self.height:
                self.x = 1
                # self.end = True we dont want this here blyat
            animation_list, speed_list = self.animation_func
            self.y = int(animation_list[self.x]) + self.offset
            self.x += self.speed + int(speed_list[self.x])
        else:
            if self.y >= self.width:
                self.y = 0
                self.end = True
            animation_list, speed_list = self.animation_func
            self.x = int(animation_list[self.y])
            self.y += self.speed + int(speed_list[self.y])

    def prepare_animation(self, animation):
        """Interpolate image movement and speed function."""
        x = range(self.width)
        xp = [x*(self.width - self.dim[1]) for x in self.curves[animation][0]]
        fp = [x*(self.height - self.dim[0]) for x in self.curves[animation][1]]
        speed_diff = [x for x in self.curves[animation][2]]
        return np.interp(x, xp, fp), np.interp(x, xp, speed_diff)

    def prepare_animation_inverse(self, animation):
        """Interpolate image movement and speed function."""
        x = range(self.height)
        xp = [x*(self.height - self.dim[0]) for x in self.curves[animation][0]]
        fp = [x*(self.width - self.dim[1]) for x in self.curves[animation][1]]
        speed_diff = [x for x in self.curves[animation][2]]
        return np.interp(x, xp, fp), np.interp(x, xp, speed_diff)
