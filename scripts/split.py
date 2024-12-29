import os
from moviepy import VideoFileClip


SOURCE_PATH = '../dataset/cropped/'
TRAIN_PATH = '../dataset/train/1_O/'
TEST_PATH = '../dataset/test/'

SKIP = 0.7


# Reference: https://www.youtube.com/watch?v=dzkC0JjfZIM
def split(file, adjustment=0):
    video = VideoFileClip(file)

    start = SKIP
    end = video.duration - SKIP
    mid = ((start+end)/2)+adjustment
    
    v1 = video.subclipped(start, mid)
    v2 = video.subclipped(mid, end)
    train_filename = TRAIN_PATH+file.split('/')[3].replace('.mp4', '_O.mp4')
    test_filename = TEST_PATH+file.split('/')[3]
    v1.write_videofile(train_filename, codec = 'libx264')
    v2.write_videofile(test_filename, codec = 'libx264')

    
def splitAllVideos():
    if not os.path.isdir(TRAIN_PATH):
        os.makedirs(TRAIN_PATH)

    if not os.path.isdir(TEST_PATH):
        os.makedirs(TEST_PATH)        

    for filename in os.listdir(SOURCE_PATH):
        if filename.endswith('mp4'):
            f = os.path.join(SOURCE_PATH, filename)
            print('Splitting ' + f.split('/')[3])
            split(f)


# Adjusting videos whose split wasn't correct
def adjustSplits():
    split(os.path.join(SOURCE_PATH, 'ancient.mp4'), -1.0)
    split(os.path.join(SOURCE_PATH, 'continuously.mp4'), 0.5)
    split(os.path.join(SOURCE_PATH, 'do.mp4'), -0.7)
    split(os.path.join(SOURCE_PATH, 'request.mp4'), 1.0)
    split(os.path.join(SOURCE_PATH, 'she.mp4'), -1.0)
    split(os.path.join(SOURCE_PATH, 'woman.mp4'), -0.5)


splitAllVideos()

adjustSplits()