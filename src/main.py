from src.computer_vision.video_stabilization.video_stabilization import video

video = video(stabilize=True)

# Declarem loop infinit
while True:
    frame = video.get_frame()
    video.show_frame(frame)
