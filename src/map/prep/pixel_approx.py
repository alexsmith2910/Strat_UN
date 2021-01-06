from secrets import choice
from PIL import Image
import os
from os import listdir
from os.path import isfile, join

#import os
script_loc = (os.path.dirname(os.path.realpath(__file__)))
script_loc = script_loc[:-4]

def get_noise():
    onlyfiles = [f for f in listdir(script_loc + "\\generated") if isfile(join(script_loc + "\\generated", f))]
    #print(onlyfiles)
    chosen = script_loc + "\\generated\\" + str(choice(onlyfiles))
    img = Image.open(chosen)
    # img = Image.open("c:/users/sebas/downloads/KmFDqavv_o.jpg") # Manual override
    return img


def tileize(image_to_transform, tile_size):
    output_image=image_to_transform.convert("L") # converts to grayscale
    listed = []
    tileised_res = ((output_image.height//tile_size), (output_image.width//tile_size))
    for x in range(tileised_res[1]):
        listed.append([])
        for y in range(tileised_res[0]):
            listed[len(listed)-1].append([])

    xcount = 0
    ycount = 0

    # print(len(listed))
    # print(len(listed[0]))
    for x in range((output_image.width//tile_size)):
        ycount = 0
        if x > 0:
            xcount += 1
        for y in range(output_image.height):
            if (y) % tile_size == 0:
                ycount += 1
                if ycount == 50:
                    break
                if y == 0:
                    ycount = 0
                # listed[]
                # print(xcount, ycount)
                for countx, x in enumerate(range(tile_size)):
                    for county, y in enumerate(range(tile_size)):
                        # print(xcount, ycount)
                        listed[xcount][ycount].append(output_image.getpixel(((20*xcount)+countx, (20*ycount)+county)))
                # try:
                #     (listed[ycount][xcount]).append(output_image.getpixel((x, y)))
                # except:
                #     print("error at:", xcount, ycount)
    processed = []
    for i in listed:
        processed.append([])
        for countj, j in enumerate(i):
            processed[len(processed)-1].append([])
            total = 0
            for k in j:
                total += k
            processed[len(processed)-1][countj].append(total//tile_size**2)


    # print(listed)
    return processed

# print(map := tileize(get_noise(), 20))
# print(len(map))
# print(len(map[0]))