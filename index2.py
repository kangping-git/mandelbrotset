import cupy
from PIL import Image
import cv2
w = 1000
h = 1000
zoom = (w+h)/8
def im(X,Y,I,zoom,XX):
    Z = cupy.zeros(w*h,cupy.complex128)
    Z = Z.reshape(w,h)
    C = (w/2-cupy.tile(cupy.arange(0,w),h))/zoom-Y
    C = C.reshape(w,h)
    C_ = (h/2-cupy.arange(0,h))/zoom-X
    C_ = C_.repeat(w)
    C_ = C_.reshape(w,h)
    C = C*1j + C_
    L = cupy.zeros(w*h,cupy.int8)
    L = L.reshape(w,h)
    for i in range(XX):
        Z *= Z
        Z += C
        Z2 = abs(Z) >= 4
        L = L + (Z2.astype("int8")*(i * (1/(2000/100)))).astype("int8")
        Z -= Z2.astype("complex128")*Z
        C -= Z2.astype("complex128")*C
    Z = L == 0
    Z = 255-(Z.astype("uint8")*255)
    Z_ = L != 0
    Z = Z + (((255-L.astype("uint8")*100)*Z_.astype("uint8")).astype("uint8"))
    img = Image.fromarray(cupy.asnumpy(cupy.rot90(Z,3)))
    img.save("./img2/" + str(w) + "x" + str(h) + "x" + str(I) + ".png")
    outimg_files.append("./img2/" + str(w) + "x" + str(h) + "x" + str(I) + ".png")
outimg_files = []
i = 0
while True:
    if zoom < 2500000:
        im((w-144.42)/500,0,i,zoom,500)
        outimg_files.append("./img2/" + str(w) + "x" + str(h) + "x" + str(i) + ".png")
        zoom *= 1.05
        print(i)
        i += 1
    else:
        break
k = 144.42
while True:
    if k > 144.30002:
        im((w-k)/500,0,i,zoom,500)
        outimg_files.append("./img2/" + str(w) + "x" + str(h) + "x" + str(i) + ".png")
        print(i)
        k -= 0.001
        i += 1
    else:
        break
while True:
    if zoom < 10000000000:
        im((w-144.30002)/500,0,i,zoom,1000)
        outimg_files.append("./img2/" + str(w) + "x" + str(h) + "x" + str(i) + ".png")
        zoom *= 1.05
        print(i)
        i += 1
    else:
        break
while True:
    if zoom < 50000000000:
        im((w-144.30002)/500,0,i,zoom,2000)
        outimg_files.append("./img2/" + str(w) + "x" + str(h) + "x" + str(i) + ".png")
        zoom *= 1.05
        print(i)
        i += 1
    else:
        break
fourcc = cv2.VideoWriter_fourcc('m','p','4', 'v')
video  = cv2.VideoWriter('video.mov', fourcc, 60.0, (w, h))

for img_file in outimg_files:
    img = cv2.imread(img_file)
    video.write(img)
for i in range(60):
    img = cv2.imread(outimg_files[-1])
    video.write(img)
video.release()