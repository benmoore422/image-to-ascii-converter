from PIL import Image
import numpy as np
import math
import sys, random, argparse 

# 70 levels of gray
gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
gscale2 = '@%#*+=-:. '

def getAverageGreysacleVal(img):
    im = np.array(img)
    width, height = im.shape

    return np.average(im.reshape(width * height))

def convertImg2Ascii(fname, moreLvls):
    global gscale1, gscale2

    img = Image.open(fname).convert('L')
    imgWidth, imgHeight = img.size[0], img.size[1]

    cols = 80
    scale = 0.43
    width = imgWidth/cols
    height = width/scale

    rows = int(imgHeight/height)

    if cols > imgWidth or rows > imgHeight:
        print("Image to small for specified rows or columns")
        exit(0)

    aimg = []

    # for every row
    for r in range(rows):
        y1 = (int)(r*height)
        y2 = (int)((r+1)*height)

        if r == rows-1:
            y2 = imgHeight

        aimg.append("")

        for i in range(cols):
            x1 = int(i * width)
            x2 = int((i+1) * width)

            if i == cols-1:
                x2 = imgWidth

            finalImg = img.crop((x1, y1, x2, y2))

            avg = int(getAverageGreysacleVal(finalImg))

            if moreLvls:
                gval = gscale1[int((avg*69)/255)]
            else:
                gval = gscale1[int((avg*69)/255)]

            aimg[r] += gval

    return aimg


def main():
    # get width and height of image
    desc = "Convert image ti ASCII art"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--file', dest='imgFile', required=True)
    parser.add_argument('--out', dest='outFile', required=False)
    parser.add_argument('--moreLevels', dest='moreLevels', required=False)

    args = parser.parse_args()

    imgFile = args.imgFile

    outFile = 'out.txt'
    if args.outFile:
        outFile = args.outFile

    moreLevels = False
    
    if args.moreLevels:
        moreLevels = args.moreLevels

    aimg = convertImg2Ascii(imgFile, moreLevels) 

    f = open(outFile, "w")

    for row in aimg:
        f.write(row + '\n')

    f.close()
    print("Success!")


if __name__ == '__main__':
    main()
