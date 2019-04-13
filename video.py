import cv2

from shape import Shape
from subtitles import Subtitles
from effect import Effect
from random import randint


class Video:
    def __init__(self,
                 video_file="./data/videos/Pexels Videos 5004.mp4",
                 width=1920,
                 height=1080,
                 FPS=60,
                 text="FAST\nFURIOUS\nFANCY",
                 title="Topanka",
                 image_paths=[
                     "data/pictures/topanka.png",
                     "data/pictures/topanka.png"
                 ],
                 text_speed=20,
                 font=None,
                 speed=6,
                 color_effect="red",
                 animation="curve2",
                 multi=False,
                 render=False,
                 output="output.mp4"):
        self.video_file = video_file
        self.width = width
        self.height = height
        self.FPS = FPS
        self.text = text
        self.title = ""
        words = title.split(" ")
        if len(words) > 3:
            cnt = 0
            for i in range(len(words)):
                self.title += words[i]
                cnt += 1
                if cnt == 3:
                    cnt = 0
                    self.title += "\n"
                else:
                    self.title += " "
        else:
            self.title = title

        self.image_paths = image_paths
        self.text_speed = text_speed
        self.font = font
        self.speed = speed
        self.color_effect = color_effect
        self.animation = animation
        self.multi = multi
        self.render = render
        self.output = output

        self.paint_x = 0
        self.paint_y = 0

    def play(self):
        # Create a VideoCapture object and read from input file
        # If the input is the camera, pass 0 instead of the video file name
        cap = cv2.VideoCapture(self.video_file)

        # Check if camera opened successfully
        if cap.isOpened() is False:
            print("Error opening video stream or file")
        index = 0

        # find out the video dimensions
        self.height, self.width, _ = cap.read()[1].shape

        if not self.multi:
            shape = Shape(
                self.width,
                self.height,
                self.paint_x,
                self.paint_y,
                self.speed,
                self.image_paths[index % len(self.image_paths)],
                self.animation,
            )
        else:
            shapes = [Shape(
                self.width,
                self.height,
                randint(0, self.width),
                randint(0, self.height),
                # int(self.height / 4 * (i + 1)),
                # int(self.width / (4 * (i + 1))),
                self.speed,
                image,
                "fall",  # must be with fall!!! it's 02:03am
            ) for i, image in enumerate(self.image_paths[:4])]

        effect = Effect(self.color_effect)
        text = Subtitles(self.text, self.text_speed,
                         acceleration=3, font=self.font)
        # text = Subtitles('FAST\nFURIOUS\nFANCY', self.text_speed,
        #                  './data/fonts/Dogfish/Dogfish.ttf')

        title = Subtitles(self.title, self.text_speed, font=self.font)
        title.font_scale = 3
        title.thick = 3
        # Read until video is completed

        # Default resolutions of the frame are obtained.The default resolutions
        # are system dependent. We convert the resolutions from float to
        # integer.
        # frame_width = int(cap.get(3))
        # frame_height = int(cap.get(4))

        # print("width ", frame_width)
        # print("height ", frame_height)
        out = cv2.VideoWriter(self.output, cv2.VideoWriter_fourcc(*'MP4V'),
                              17, (self.width, self.height))

        while cap.isOpened():
            # Capture frame-by-frame
            ret, frame = cap.read()
            try:
                self.width = frame.shape[1]
                self.height = frame.shape[0]
            except AttributeError:
                break

            if ret is True:
                frame = effect.apply(frame)
                if self.multi:
                    for shape in shapes:
                        shape.paint(frame)
                else:
                    shape.paint(frame)
                    pass

                frame = title.show_title(frame, self.width, self.height)
                # frame = text.show_low(frame, self.width, self.height)
                frame = text.show_price(frame, self.width, self.height)
                # if title.counter == 1:
                #     text.counter = title.counter
                if self.render:
                    cv2.imshow("Frame", frame)
                out.write(frame)
                if not self.multi and shape.end:
                    index += 1
                    if index >= len(self.image_paths):
                        index = 0

                    shape = Shape(
                        self.width,
                        self.height,
                        self.paint_x,
                        self.paint_y,
                        self.speed,
                        self.image_paths[index % len(self.image_paths)],
                        self.animation,
                    )

                # Press Q on keyboard to  exit
                if cv2.waitKey(25) & 0xFF == ord("q"):
                    return
            # Break the loop
            else:
                break

        # When everything done, release the video capture object
        cap.release()

        # Closes all the frames
        cv2.destroyAllWindows()
