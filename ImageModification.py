
# On PPM and PGM formats see http://paulbourke.net/dataformats/ppm/
# On convolution operation see https://youtu.be/KiftWz544_8
# To view .pgm and .ppm files, you can use IrfanView, see https://www.irfanview.com/

filename = input()
operation = int(input())


def img_printer(img):
    row = len(img)
    col = len(img[0])
    cha = len(img[0][0])
    for i in range(row):
        for j in range(col):
            for k in range(cha):
                print(img[i][j][k], end=" ")
            print("\t|", end=" ")
        print()


handle = open(filename)
form = handle.readline().strip()
col_num , row_num = handle.readline().split()
col_num , row_num = int(col_num) , int(row_num)
resolution = int(handle.readline().strip())
p = handle.read().split()
handle.close()
if form == "P3":
    pixels = [[[0, 0, 0] for c in range(col_num)] for r in range(row_num)]
else:
    pixels = [[[0] for c in range(col_num)] for r in range(row_num)]
count = 0
row = len(pixels)
col = len(pixels[0])
cha = len(pixels[0][0])
for i in range(row):
    for j in range(col):
        for k in range(cha):
            pixels[i][j][k] = int(p[count])
            count += 1


if operation == 1:
    colored = dict()
    averaged = dict()
    for i in range(row_num):
        for j in range(col_num):
            colored[(i,j)] , averaged[(i,j)] = False , False
    def average(pix,row,col,sum_els):
        global averaged
        global col_num
        global row_num
        if averaged.get((row,col)) == True or (col not in range(col_num)) or (row not in range(row_num)):
            return
        if pix[row][col][0] == 0:
            return
        sum_els[0] += pix[row][col][0]
        sum_els[1] += 1
        averaged[(row,col)] = True
        neighs = [(1,0),(0,1),(-1,0),(0,-1)]
        for a,b in neighs:
            average(pix,row+a,col+b,sum_els)
        return sum_els[0]//sum_els[1]


    def color(pix,row,col,colour):
        global colored
        global col_num
        global row_num
        if colored.get((row, col)) == True or (col not in range(col_num)) or (row not in range(row_num)):
            return
        if pix[row][col][0] == 0:
            return
        pix[row][col][0] = colour
        colored[(row,col)] = True
        neighs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        for a, b in neighs:
            color(pix, row + a, col + b, colour)

    for i in range(row_num):
        for j in range(col_num):
            if averaged[(i,j)] == False and not pixels[i][j][0]==0:
                avg_color = average(pixels,i,j,[0,0])
                color(pixels,i,j,avg_color)
    img_printer(pixels)



elif operation == 2:
    hand = open(input())
    stride = int(input())
    filt = hand.readlines()
    hand.close()
    size = len(filt)
    kernel = [[0 for c in range(size)] for r in range(size)]
    for r in range(size):
        for c in range(size):
            kernel[r][c] = float(filt[r].split()[c])
    neighs = []
    for r in range(size//2 * -1,size//2 + 1):
        for c in range(size // 2 * -1, size // 2 + 1):
            if not (c == 0 and r == 0):
                neighs.append([r,c])
    kernel_center = [size//2,size//2]
    def filtering(row,col,cha,image,kern,kern_cen,result=[[]]):
        global neighs
        global stride
        if row + len(kern)//2 >= len(image):
            return result
        summ = 0
        a,b = kern_cen
        summ += image[row][col][cha] * kern[a][b]
        try:
            for x,y in neighs:
                summ += image[row+x][col+y][cha] * kern[a+x][b+y]
            summ = int(summ//1)
            if summ in range(0,256):
                result[-1] += [summ]
            elif summ < 0:
                result[-1] += [0]
            else:
                result[-1] += [255]
            filtering(row,col+stride,cha,image,kern,kern_cen,result)
        except:
            result += [[]]
            filtering(row+stride,b,cha,image,kern,kern_cen,result)
        return result


    red = filtering(kernel_center[0],kernel_center[1],0,pixels,kernel,kernel_center,[[]])[:-1]
    green = filtering(kernel_center[0],kernel_center[1],1,pixels,kernel,kernel_center,[[]])[:-1]
    blue = filtering(kernel_center[0],kernel_center[1],2,pixels,kernel,kernel_center,[[]])[:-1]
    row_num = len(red)
    col_num = len(red[0])
    new_img = [[[0, 0, 0] for c in range(col_num)] for r in range(row_num)]
    for r in range(row_num):
        for c in range(col_num):
            new_img[r][c][0] = red[r][c]
            new_img[r][c][1] = green[r][c]
            new_img[r][c][2] = blue[r][c]
    img_printer(new_img)

