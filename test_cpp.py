from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
import numpy as np
import sys


def plot_linear_cube(bb, ax, color):
    '''
    :param bb: list, bounding box with 2 coordinates(front bottom left corner and back top right corner)
    :param ax: figure
    :param color: string
    '''

    # extract front bottom left point
    x = bb[0]
    y = bb[1]
    z = bb[2]

    # compute side_length
    dx = bb[3] - bb[0]
    dy = bb[4] - bb[1]
    dz = bb[5] - bb[2]

    # draw side by side
    xx = [x, x, x+dx, x+dx, x]
    yy = [y, y+dy, y+dy, y, y]
    ax.plot3D(xx, yy, [z] * 5, color)
    ax.plot3D(xx, yy, [z + dz] * 5, color)
    ax.plot3D([x, x], [y, y], [z, z + dz], color)
    ax.plot3D([x, x], [y + dy, y + dy], [z, z + dz], color)
    ax.plot3D([x + dx, x + dx], [y + dy, y + dy], [z, z + dz], color)
    ax.plot3D([x + dx, x + dx], [y, y], [z, z + dz], color)


def plot_linear_sphere(radius, center, ax, color):
    '''
    :param radius: float, sphere's radius
    :param center: float, sphere's center
    :param ax: figure
    :param color: string
    '''
    u = np.linspace(0, 2 * np.pi, 20)
    v = np.linspace(0, np.pi, 20)
    x = radius * np.outer(np.cos(u), np.sin(v)) + center[0]
    y = radius * np.outer(np.sin(u), np.sin(v)) + center[1]
    z = radius * np.outer(np.ones(np.size(u)), np.cos(v)) + center[2]

    # Plot the skeleton
    ax.plot_wireframe(x, y, z, color=color)


if __name__ == "__main__":
    sys.path.insert(0, 'nms_cpp/x64/Debug')
    import nms_cpp

    fig = plt.figure()
    ax = fig.add_subplot(121, projection='3d')

    # draw a sphere
    plot_linear_sphere(10, [0, 0, 0], ax, color='blue')
    plot_linear_sphere(1, [-11, -11, -11], ax, color='blue')

    # create and draw bounding boxes
    bbs = []
    scores = []

    bb1 = [-10.0, -10.0, -10.0, 10.0, 10.0, 10.0]  # first three numbers correspond to the coordinate of the front left bottom point, last three numbers are the coordinate of the back top right point
    bbs.append(bb1)
    scores.append(0.9)  # assign a random score for test
    plot_linear_cube(bb1, ax, color='red')  # draw bounding box
    ax.text(bb1[0], bb1[1], bb1[2] + bb1[3] - bb1[0], scores[0], color='red')  # display score

    bb2 = [-9.0, -9.0, -9.0, 11.0, 11.0, 11.0]
    bbs.append(bb2)
    scores.append(0.7)
    plot_linear_cube(bb2, ax, color='yellow')
    ax.text(bb2[0], bb2[1], bb2[2] + bb2[3] - bb2[0], scores[1], color='yellow')

    bb3 = [-11.0, -11.0, -11.0, 9.0, 9.0, 9.0]
    bbs.append(bb3)
    scores.append(0.8)
    plot_linear_cube(bb3, ax, color='green')
    ax.text(bb3[0], bb3[1], bb3[2] + bb3[3] - bb3[0], scores[2], color='green')

    bb4 = [-12.0, -12.0, -12.0, -10.0, -10.0, -10.0]
    bbs.append(bb4)
    scores.append(0.7)
    plot_linear_cube(bb4, ax, color='red')
    ax.text(bb4[0], bb4[1], bb4[2] + bb4[3] - bb4[0], scores[3], color='red')

    # compute result bounding boxes
    bb_score = nms_cpp.nms_3d(bbs, scores, 0.5)
    res_box = bb_score.res_boxes
    res_score = bb_score.res_scores
    print(res_box)

    # display results
    ax2 = fig.add_subplot(122, projection='3d')
    plot_linear_sphere(10, [0, 0, 0], ax2, color='blue')
    plot_linear_sphere(1, [-11, -11, -11], ax2, color='blue')

    for i in range(len(res_box)):
        plot_linear_cube(res_box[i], ax2, color='purple')
        ax2.text(res_box[i][0], res_box[i][1], res_box[i][2] + res_box[i][3] - res_box[i][0], round(res_score[i], 1), color='purple')

    plt.show()