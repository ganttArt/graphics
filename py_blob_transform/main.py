from pathlib import Path
from PIL import Image
import numpy as np
import cv2
import os


def create_np_array(pil_image):
    '''converts a jpg to a numpy array'''
    return np.array(pil_image)


def pixel_is_edge(row, column, image_one, image_two):
    if image_one[row][column][0] == image_two[row][column][0]:
        return False

    is_edge = False
    target_pixel = image_one[row][column][0]
    # print('pixel is edge', row, column)
    for i in range(row - 1, row + 2):
        # print('row', i)
        for j in range(column - 1, column + 2):
            # print('column', j)
            if image_one[i][j][0] != target_pixel:
                is_edge = True
                break

    return is_edge


def create_frame(image_one, image_two):
    '''
      image_one, image_two : numpy array
    '''
    dimensions = image_one.shape
    new_frame = np.copy(image_one)
    height = dimensions[0]
    width = dimensions[1]

    for i in range(1, height - 1):
        if i % 200 == 0:
            print(f'Row {i} of {height - 1}')
        for j in range(1, width - 1):
            if pixel_is_edge(i, j, image_one, image_two):
                # print('new frame', new_frame[i][j])
                # print('image_two', image_two[i][j])
                new_frame[i-1][j-1] = image_two[i-1][j-1]
                new_frame[i-1][j] = image_two[i-1][j]
                new_frame[i-1][j+1] = image_two[i-1][j+1]
                new_frame[i][j-1] = image_two[i][j-1]
                new_frame[i][j] = image_two[i][j]
                new_frame[i][j+1] = image_two[i][j+1]
                new_frame[i+1][j-1] = image_two[i+1][j-1]
                new_frame[i+1][j] = image_two[i+1][j]
                new_frame[i+1][j+1] = image_two[i+1][j+1]

    int_array = new_frame.astype(np.uint8)
    return Image.fromarray(int_array)


def create_many_images(image_one, image_two):
    file_id = 1000001
    count = 1
    while True:
        if np.array_equal(image_one, image_two):
            break
        print("Frame #", count)
        FRAME = create_frame(image_one, image_two)
        save_file(FRAME, f'{file_id}.png')
        file_id += 1
        count += 1
        image_one = create_np_array(FRAME)
    return


def save_file(pil_image, filename):
    pil_image.save(f'{filename}')
    return


def create_video(video_filename, fps):
    image_folder = 'video-frames'
    output_name = video_filename + '.mp4'

    images = sorted([img for img in os.listdir(image_folder)])
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(output_name,
                            cv2.VideoWriter_fourcc(*'mp4v'),
                            fps,
                            (width, height))

    count = 1
    for image in images:
        print(count)
        video.write(cv2.imread(os.path.join(image_folder, image)))
        count += 1

    cv2.destroyAllWindows()
    video.release()
    print(f'{output_name} built')


if __name__ == "__main__":
    IMAGE_ONE = create_np_array(Image.open("assets/pony.png"))
    # print('image one', IMAGE_ONE)
    IMAGE_TWO = create_np_array(Image.open("assets/tri.png"))
    # print('image two', IMAGE_TWO)
    create_many_images(IMAGE_ONE, IMAGE_TWO)
    # FRAME = create_frame(IMAGE_ONE, IMAGE_TWO)
    # save_file(FRAME, 'new.png')

    # create_video('new', 60)
