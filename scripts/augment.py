from skimage.util import random_noise
from enum import Enum
import numpy as np
import cv2
import os
 

SOURCE_PATH = '../dataset/train/1_O'


class Augmentation(Enum):
    NOISE = 1
    TRANSLATION = 2
    ROTATION = 3
    SCALING = 4
    FLIPPING = 5
    BRIGHTNESS_CONTRAST = 7
    COLOR = 7
    

TRANSLATION_FACTOR = 10
ROTATION_ANGLE = 10
SCALE_PERCENT = 75


def check_and_create_dir(type):
    dir_name = SOURCE_PATH.replace('train', 'augmentation')
    if type == Augmentation.NOISE:
        dir_name = dir_name.replace('_O', '_N')
    elif type == Augmentation.TRANSLATION:
        dir_name = dir_name.replace('_O', '_T')
    elif type == Augmentation.ROTATION:
        dir_name = dir_name.replace('_O', '_R')
    elif type == Augmentation.SCALING:
        dir_name = dir_name.replace('_O', '_S')
    elif type == Augmentation.FLIPPING:
        dir_name = dir_name.replace('_O', '_F')
    elif type == Augmentation.BRIGHTNESS_CONTRAST:
        dir_name = dir_name.replace('_O', '_B')
    elif type == Augmentation.COLOR:
        dir_name = dir_name.replace('_O', '_C')
    
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)


def get_new_name(video, type):
    if type == Augmentation.NOISE:
        return video.replace('train', 'augmentation').replace('_O', '_N')
    elif type == Augmentation.TRANSLATION:
        return video.replace('train', 'augmentation').replace('_O', '_T')
    elif type == Augmentation.ROTATION:
        return video.replace('train', 'augmentation').replace('_O', '_R')
    elif type == Augmentation.SCALING:
        return video.replace('train', 'augmentation').replace('_O', '_S')
    elif type == Augmentation.FLIPPING:
        return video.replace('train', 'augmentation').replace('_O', '_F')
    elif type == Augmentation.BRIGHTNESS_CONTRAST:
        return video.replace('train', 'augmentation').replace('_O', '_B')
    elif type == Augmentation.COLOR:
        return video.replace('train', 'augmentation').replace('_O', '_C')


# Reference: https://scikit-image.org/docs/stable/api/skimage.util.html#random-noise
def noisy_image(image):
    noise_img = random_noise(image, mode='s&p', amount=0.05)
    return np.array(255*noise_img, dtype = 'uint8')


# Reference: https://www.geeksforgeeks.org/image-translation-using-opencv-python/
def translate_image(image, factor):
    height, width = image.shape[:2]
    new_height, new_width = 1 , width/factor
    T = np.float32([[1, 0, new_width], [0, 1, new_height]])
    return cv2.warpAffine(image, T, (width, height))


def rotate_image(image, angle):
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D((cX, cY), angle, 1.0)
    return cv2.warpAffine(image, M, (w, h))


def pad_zeroes(image, original_shape):
    height_diff = original_shape[0] - image.shape[0]
    top = int(height_diff/2)
    bottom = height_diff - top
    width_diff = original_shape[1] - image.shape[1]
    left = int(width_diff/2)
    right = width_diff - left
    return cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=0)


def scale_image(image, scale_percent):
    original_shape = image.shape
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    scaled_image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    return pad_zeroes(scaled_image, original_shape)


def flip_image(image):
    return cv2.flip(image,1)


# https://docs.opencv.org/3.4/d3/dc1/tutorial_basic_linear_transform.html
def bright_contrast_image(image):
    return cv2.convertScaleAbs(image, alpha=1.5, beta=5)    # alpha and beta are the simple contrast and brightness control respectively


def color_image(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2LUV)


def augment_frame(image, type):
    if type == Augmentation.NOISE:
        return noisy_image(image)        
    elif type == Augmentation.TRANSLATION:
        return translate_image(image, TRANSLATION_FACTOR)
    elif type == Augmentation.ROTATION:
        return rotate_image(image, ROTATION_ANGLE)
    elif type == Augmentation.SCALING:
        return scale_image(image, SCALE_PERCENT)
    elif type == Augmentation.FLIPPING:
        return flip_image(image)
    elif type == Augmentation.BRIGHTNESS_CONTRAST:
        return bright_contrast_image(image)
    elif type == Augmentation.COLOR:
        return color_image(image)


def augment_video(video, type):
    cap = cv2.VideoCapture(video)

    w_frame, h_frame = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps, frames = cap.get(cv2.CAP_PROP_FPS), cap.get(cv2.CAP_PROP_FRAME_COUNT)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    new_name = get_new_name(video, type)
    out = cv2.VideoWriter(new_name, fourcc, fps, (w_frame, h_frame))

    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret==True:
            frame = augment_frame(frame, type)
            out.write(frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()


def augment_all_videos(type):
    check_and_create_dir(type)

    for filename in os.listdir(SOURCE_PATH):
        if '_O' in filename:
            file = os.path.join(SOURCE_PATH, filename)
            if os.path.isfile(file):
                print('Augmenting ' + file)
                augment_video(file, type)


# augment_all_videos(Augmentation.NOISE)
augment_all_videos(Augmentation.TRANSLATION)
# augment_all_videos(Augmentation.ROTATION)
# augment_all_videos(Augmentation.SCALING)
# augment_all_videos(Augmentation.FLIPPING)
# augment_all_videos(Augmentation.BRIGHTNESS_CONTRAST)
# augment_all_videos(Augmentation.COLOR)