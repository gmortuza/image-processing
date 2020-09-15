import numpy as np
import PIL
import matplotlib.pyplot as plt

def load_image(path):
    """
    Convert and image to an numpy array.
    It will return the padded image.
    Each axis will be padded with zero
    """
    img = np.asarray(PIL.Image.open(path))
    return np.pad(img, (1, 1), mode='constant', constant_values=(0, 0))

isri = load_image('isri_5g.gif')
skull = load_image('skull.gif')

connected_component = np.zeros(isri.shape).astype(int)

label = 0
for row in range(1, isri.shape[0]):
    for col in range(1, isri.shape[1]):
        if isri[row, col] == 0:
            continue
        # Check it's neighbour
        top = connected_component[row-1, col]
        left = connected_component[row, col-1]
        top_left = connected_component[row-1, col-1]
        top_right = connected_component[row-1, col+1]
        neighbours = [top, left, top_right, top_left]
        if top == left == top_left == top_right == 0:
            # Set new label
            label += 1
            put_label = label
        elif (left == top == 0 and top_left != 0 and top_right != 0) or \
            (top_left == top == 0 and left != 0 and top_right != 0) or \
            (top == 0 and left != 0 and top_left != 0 and top_right != 0):
            put_label = min(neighbours)
            for val in neighbours:
                connected_component = np.where(connected_component == val, put_label, connected_component)
        else:
            put_label = min(neighbours)

        connected_component[row, col] = put_label
connected_component = connected_component[1:-1, 1:-1]

connected_component = np.pad(connected_component, (1, 1), mode='constant', constant_values=(0, 0))

# draw bounding boxes on connected component
bb_connected_component = np.zeros(connected_component.shape)
# add padding
for row in range(1, bb_connected_component.shape[0]):
    for col in range(1, bb_connected_component.shape[1]):
        if connected_component[row, col] != 0:
            # check top
            bb_connected_component[row-1, col] = 1 if connected_component[row-1, col] == 0 else 0
            # check bottom
            bb_connected_component[row+1, col] = 1 if connected_component[row+1, col] == 0 else 0
            # check left
            bb_connected_component[row, col-1] = 1 if connected_component[row, col-1] == 0 else 0
            # check right
            bb_connected_component[row, col+1] = 1 if connected_component[row, col+1] == 0 else 0

bb_connected_component = bb_connected_component[1:-1, 1:-1]