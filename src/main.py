from src.computer_vision.video_stabilization.video_stabilization import video
import cv2

video_options = {
    "CAP_PROP_FRAME_WIDTH": 640,
    "CAP_PROP_FRAME_HEIGHT": 480,
    "CAP_PROP_FPS": 10,
}

# Declaració objecte classe video que ens permet obtenir imatges de la camera.
video = video(stabilize=False, record=True, detect_people=True, video_options=video_options)

# Declarem loop infinit
while True:

    frame = video.get_frame()
    video.show_frame(frame)

    # check for 'q' key if pressed
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
