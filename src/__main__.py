from camera import Camera

def __main__() -> None:
    cam = Camera("192.168.1.4", "8080", "admin", "123456789", 63)
    cam.run()
   

if __name__ == "__main__":
    __main__()
