from PIL import Image
import decimal
import cv2
from multiprocessing import Process
w = 1000
h = 1000
X = 0
Y = 0
zoom = decimal.Decimal(int(h/2.5))
loopCount = 100
decimal.getcontext().prec = 100
img = Image.new("RGB", (w, h),(255,255,255))
def func(y):
    for x in range(h):
        Z = [decimal.Decimal(0),decimal.Decimal(0)]
        C = [(decimal.Decimal(y)-decimal.Decimal(w)/2)/zoom-X,-(decimal.Decimal(x)-decimal.Decimal(h)/2)/zoom-Y]
        flg = False
        for i in range(loopCount):
            Z = [(Z[0] ** decimal.Decimal(2)) - (Z[1] ** decimal.Decimal(2)) + C[0],Z[0] * Z[1] * decimal.Decimal(2)+C[1]]
            if (Z[0] ** 2 + Z[1] ** 2 > 4):
                flg = True
                if i < loopCount/3:
                    img.putpixel((y,x),(int(i * (256 / (loopCount / 3))),int(i * (256 / (loopCount / 3))),int(255-(i * (256 / (loopCount / 3))))))
                elif i < loopCount * 2/3:
                    img.putpixel((y,x),(255,int(255-(i-loopCount/3)*(256 / (loopCount / 3))),255))
                else:
                    img.putpixel((y,x),(255,int(255-(i-loopCount/3)*(256 / (loopCount / 3))),int(255-(i-loopCount/3)*(256 / (loopCount / 3)))))
                break
        if not flg:
            img.putpixel((y,x),(0,0,0))
outimg_files = []
def task(i):
    global zoom,X
    for y in range(w):
        func(y)
        print(str((y/w)*100) + "%")
    img.save("./img/" + str(i) + ".png")
    # zoom *= decimal.Decimal(1.1)
    # if i < 31:
    #     X = (-decimal.Decimal(i/100) ** 2 + 2 * decimal.Decimal(i/100)) * decimal.Decimal(1.8038469627200018)*2
    # print(i)
    # outimg_files.append("./img/" + str(i) + ".png")
task(0)