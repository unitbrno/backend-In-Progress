import cv2


class Subtitles:
    """docstring for."""

    def __init__(self, text, speed=20, acceleration=6,
                 font='./data/fonts/Flanella/Flanella.ttf'):
        self.acceleration = acceleration
        self.lines = text.replace("/ ", "/").splitlines() if text else " "
        self.length = len(self.lines)
        self.speed = speed
        self.font = font
        self.index = 0
        self.counter = 0
        self.pos = 0
        # heigth
        self.font_scale = 2
        # thickeness
        self.thick = 6
        self.x = 0
        self.y = 0

    def step(self):
        if self.counter == self.speed:
            self.index = 0 if self.index >= self.length-1 else self.index + 1
            self.counter = 0
        self.counter += 1

    def get_size(self):
        return cv2.getTextSize(
            self.lines[self.index], cv2.FONT_HERSHEY_SIMPLEX,
            self.font_scale, self.thick
        )[0]

    def render(self, frame):
        cv2.putText(
            frame, self.lines[self.index].upper(),
            (self.x, self.y),
            cv2.FONT_HERSHEY_SIMPLEX,
            self.font_scale,
            (0,),
            self.thick+3,
            cv2.LINE_AA
            )
        cv2.putText(
            frame, self.lines[self.index].upper(),
            (self.x, self.y),
            cv2.FONT_HERSHEY_SIMPLEX,
            self.font_scale,
            (255, 255, 255),
            self.thick,
            cv2.LINE_AA
            )
        return frame

    def custom_font(self, frame):
        # use a truetype font
        import numpy as np
        from PIL import ImageFont, ImageDraw, Image

        font2 = ImageFont.truetype(self.font, 100)
        font = ImageFont.truetype(self.font, 100)
        pil_im = Image.fromarray(frame)
        draw = ImageDraw.Draw(pil_im)

        draw.text(
            (self.x, self.y), self.lines[self.index],
            font=font2, fill=(0, 0, 0))
        draw.text(
            (self.x-10, self.y-10), self.lines[self.index],
            font=font, fill=(255, 255, 255))

        return np.array(pil_im)

    def show_centered(self, frame, width, height):
        size = self.get_size()
        self.x = int(width/2) - int(size[0]/2)
        self.y = int(height) - int(size[1]/2)
        self.step()
        return self.render(frame)

    def show_price(self, frame, width, height):
        size = self.get_size()
        self.step()
        if self.pos + self.get_size()[0] >= width:
            self.pos = 0
        else:
            self.pos += self.acceleration
        self.x = self.pos
        self.y = height - int(size[1]*4)
        return self.custom_font(frame)

    def show_title(self, frame, width, height):
        size = self.get_size()
        self.step()
        # if self.pos + self.get_size()[0] >= width:
        #     self.pos = 0
        # else:
        #     self.pos += self.acceleration
        # self.x = self.pos
        # self.y = int(height/8) # - int(size[1]*3)
        self.x = int(width/2) - int(size[0]/2)
        self.y = int(height/2) - int(size[1]/2)
        return self.render(frame)
