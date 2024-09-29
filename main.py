import cv2
import numpy as np
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image

class CameraApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        
        self.image = Image()
        self.layout.add_widget(self.image)
        
        btn_capture = Button(text="Capture", size_hint=(1, 0.1))
        btn_capture.bind(on_press=self.capture)
        self.layout.add_widget(btn_capture)
        
        self.capture_camera()
        
        return self.layout

    def capture_camera(self):
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0 / 30.0)

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            height, width = frame.shape[:2]
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray_frame, 120, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # A4 size in pixels (adjust as necessary)
            a4_width = int(210 * (width / 1000))  
            a4_height = int(297 * (height / 1000))  

            buffer_space = 20  
            corners_touched = [False] * 4
            
            for contour in contours:
                epsilon = 0.02 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)

                if len(approx) == 4:
                    x, y, w, h = cv2.boundingRect(approx)
                    
                    if (w >= a4_width * 0.9 and w <= a4_width * 1.1) and (h >= a4_height * 0.9 and h <= a4_height * 1.1):
                        corner_coords = [
                            (x - buffer_space, y - buffer_space),                 
                            (x + w + buffer_space, y - buffer_space),             
                            (x - buffer_space, y + h + buffer_space),             
                            (x + w + buffer_space, y + h + buffer_space)         
                        ]

                        for i, (cx, cy) in enumerate(corner_coords):
                            if (0 <= cx < width) and (0 <= cy < height):
                                corners_touched[i] = True

            object_touches_all_corners = all(corners_touched)
            color = (255, 255, 255) if not object_touches_all_corners else (0, 255, 0)

            # Draw "L" shapes
            line_length = 20  
            top_left = (50, 50)
            top_right = (width - 50, 50)
            bottom_left = (50, height - 50)
            bottom_right = (width - 50, height - 50)

            for point in [top_left, top_right, bottom_left, bottom_right]:
                cv2.line(frame, point, (point[0] + line_length, point[1]), color, 2)
                cv2.line(frame, point, (point[0], point[1] + line_length), color, 2)

            buf = cv2.flip(frame, 0).tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.image.texture = texture

    def capture(self, instance):
        ret, frame = self.capture.read()
        if ret:
            cv2.imwrite("captured_image.png", frame)
            print("Image captured and saved as 'captured_image.png'")

    def on_stop(self):
        if self.capture is not None:
            self.capture.release()

if __name__ == '__main__':
    CameraApp().run()
