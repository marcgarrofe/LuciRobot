import matplotlib.pyplot as plt
import numpy as np
import cv2
import matplotlib.image as img

def mergeImage(termic, normal):
    if termic is not None and normal is not None and len(termic) > 0 and len(normal) > 0:
        normal = cv2.cvtColor(normal, cv2.COLOR_BGR2RGB)
        print("[INFO] Merging images")
        print("[INFO] Normal image shape: ", normal.shape)
        print("[INFO] Termic image shape: ", termic.shape)

        [hTermic, wTermic, cTermic] = termic.shape
        [hNormal, wNormal, cNormal] = normal.shape
        
        combine = cv2.addWeighted(termic, 0.5, normal, 0.5, 0)

        b, g, r = cv2.split(combine)

        rgb_img = cv2.merge([r, g, b])

        print("[INFO] Merged image shape: ", rgb_img.shape)

    else:
        rgb_img = normal
        
    return rgb_img

# if __name__ == '__main__':
#     termic = cv2.imread('./img/save.png', cv2.COLOR_BGR2RGB)
#     [h,w,c] = termic.shape
#     crop_image = termic[108:h-98, 147:w-159]
#     normal = cv2.imread('./img/normal.jpeg',cv2.COLOR_BGR2RGB)
#     # cv2.imshow("Crop",crop_image);
#     # cv2.waitKey(0)
#     image = mergeImage(crop_image, normal)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
