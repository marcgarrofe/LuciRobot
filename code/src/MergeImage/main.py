import matplotlib.pyplot as plt
import numpy as np
import cv2
import matplotlib.image as img

def mergeImage(termic, normal):
    [hTermic, wTermic, cTermic] = termic.shape
    [hNormal, wNormal, cNormal] = normal.shape

    plt.imshow(termic)
    plt.show()
    plt.imshow(normal)
    plt.show()

    combine = cv2.addWeighted(cv2.resize(termic, (hTermic, wTermic)), 0.5, cv2.resize(normal, (hTermic, wTermic)), 0.5, 0)

    b, g, r = cv2.split(combine)
    rgb_img = cv2.merge([r, g, b])

    plt.imshow(rgb_img)
    plt.show()

    return rgb_img

if __name__ == '__main__':
    termic = cv2.imread('./img/save.png', cv2.COLOR_BGR2RGB)
    [h,w,c] = termic.shape
    crop_image = termic[108:h-98, 147:w-159]
    normal = cv2.imread('./img/normal.jpeg',cv2.COLOR_BGR2RGB)
    # cv2.imshow("Crop",crop_image);
    # cv2.waitKey(0)
    image = mergeImage(crop_image, normal)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
