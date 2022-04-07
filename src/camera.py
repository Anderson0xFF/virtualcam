import cv2 as opencv2
import pyvirtualcam
from cv2 import VideoCapture

PIXEL = pyvirtualcam.PixelFormat.BGR

class Camera:
    def __init__(self, addrs: str, port: str, user: str, password: str, fps: int) -> None:
        self.addrs = addrs
        self.port = port
        self.user = user
        self.password = password
        self.fps = fps
        self.video = None
        self.resolution = None

    def run(self) -> None:
        self.video = self.__capture_video_network()
        
        if not Camera.video_is_opened(self.video):
            raise ValueError("Error opening video. Please check your configuration.")
        
        self.resolution = self.get_video_resolution()
        try:
            self.__run_camera()
        except:
            print("Camera stopped")

    def __run_camera(self) -> None:
        with pyvirtualcam.Camera(self.resolution[0], self.resolution[1], self.fps, fmt=PIXEL) as cam:
            Camera.__print_camera_info(cam)
            while True:
                _, frame = self.video.read()
                cam.send(frame)
                cam.sleep_until_next_frame()


    def __print_camera_info(cam) -> None:
        print("Camera running")
        print(f"Virtual camera: {cam.device}")
        print(f"Width: {cam.width} | Height: {cam.height}")
        print(f"FPS: {cam.fps}")

    def __capture_video_network(self) -> VideoCapture:
        video = opencv2.VideoCapture(
            f'rtsp://{self.user}:{self.password}@{self.addrs}:{self.port}/h264_ulaw.sdp')
        return video

    def video_is_opened(video: VideoCapture) -> bool:
        result = video.isOpened()
        return result

    def get_video_resolution(self):
        width = int(self.video.get(opencv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.video.get(opencv2.CAP_PROP_FRAME_HEIGHT))
        return (width, height)