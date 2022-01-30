from pathlib import Path
from PIL import Image
import numpy as np

def create_np_array(pil_image):
  '''converts a jpg to a numpy array'''
  return np.array(pil_image)

def change_color(row, column, image_one, image_two):
    if image_one[row][column][0] == image_two[row][column][0]:
      return False

    is_edge = False
    target_pixel = image_one[row][column][0]

    for i in range(row - 1, row + 1):
      for j in range(column - 1, column + 1):
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
    print(f'Row {i} of {height - 1}')
    for j in range(1, width - 1):
      if change_color(i, j, image_one, image_two):
        # print('new frame', new_frame[i][j])
        # print('image_two', image_two[i][j])
        new_frame[i][j] = image_two[i][j]

  int_array = new_frame.astype(np.uint8)
  return Image.fromarray(int_array)

def save_file(pil_image, filename):
  pil_image.save(f'{filename}')


if __name__ == "__main__":
  IMAGE_ONE = create_np_array(Image.open("assets/pony.png"))
  # print('image one', IMAGE_ONE)
  IMAGE_TWO = create_np_array(Image.open("assets/tri.png"))
  # print('image two', IMAGE_TWO)
  FRAME = create_frame(IMAGE_ONE, IMAGE_TWO)
  save_file(FRAME, 'new.png')
