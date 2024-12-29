import cv2
import os


SOURCE_PATH = '../dataset/original/'
CROPPED_PATH = '../dataset/cropped/'

X = 60
Y = 0
HEIGHT_FACTOR = 0
WIDTH_FACTOR = 395


def crop(file):
    video = cv2.VideoCapture(file)

    # Some characteristics from the original video
    w_frame, h_frame = int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(
        video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps, frames = video.get(cv2.CAP_PROP_FPS), video.get(
        cv2.CAP_PROP_FRAME_COUNT)

    # Define the croping values
    x, y, h, w = X, Y, h_frame-HEIGHT_FACTOR, w_frame-WIDTH_FACTOR

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(CROPPED_PATH+file.split('/')[3], fourcc, fps, (w, h))

    while (video.isOpened()):
        ret, frame = video.read()

        if ret == True:
            crop_frame = frame[y:y+h, x:x+w]
            out.write(crop_frame)
        else:
            break

    video.release()
    out.release()
    cv2.destroyAllWindows()


def cropAllVideos():
    if not os.path.isdir(SOURCE_PATH):
        print('Path doesn\'t exist: Source videos can\'t be found')
        return
    
    if not os.path.isdir(CROPPED_PATH):
        os.makedirs(CROPPED_PATH)

    for filename in os.listdir(SOURCE_PATH):
        if filename.endswith('mp4'):
            f = os.path.join(SOURCE_PATH, filename)
            print('Cropping ' + f.split('/')[3])
            crop(f)


cropAllVideos()