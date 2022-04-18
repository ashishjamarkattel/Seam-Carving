import cv2 as cv 
import numpy as np 
from tqdm import tqdm
import argparse




def energyMatrix(img):
    gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    sobel_x = cv.Sobel(gray,cv.CV_64F,1,0,ksize=3)
    sobel_y = cv.Sobel(gray,cv.CV_64F,0,1,ksize=3)
    
    abs_sobel_x = cv.convertScaleAbs(sobel_x)
    abs_sobel_y = cv.convertScaleAbs(sobel_y)
   
    return cv.addWeighted(abs_sobel_x, 0.5, abs_sobel_y, 0.5, 0) # waited energy matrix
 
    
def find_vertical_seam(img,energy):
    rows,cols = img.shape[:2]
    dist = np.zeros(energy.shape)
    dist[-1] = energy[-1]
    seam = np.zeros(rows,dtype="int32")
    for row in range(rows-2,-1,-1):
        for col in range(cols):
            if col==0:
                dist[row][col] = energy[row][col] + min(dist[row+1][col],dist[row+1][col+1])
                
            elif col == cols-1:
                dist[row][col] = energy[row][col] + min(dist[row+1][col],dist[row+1][col-1])
            else:
                dist[row][col] = energy[row][col] + min(dist[row+1][col],dist[row+1][col-1],dist[row+1][col+1])

        
    # backtracking to below

    col = np.argmin(dist[0])
    seam[0] = col
    
    for row in range(rows):
        
        if col+1>=cols-1:
            if dist[row][col]>dist[row][col-1]:
                col = col-1
            else:
                col = col
            seam[row] = col

        elif col-1<=0:
            if dist[row][col]>dist[row][col+1]:
                col = col+1
            else:
                col = col
            seam[row] = col

        else:
            minimum = dist[row][col-1]
            col = col-1
            for i in range(1,3):
                if minimum>dist[row][col+i]:
                    minimum = dist[row][col+i]
                    col = col+i 

            seam[row] = col


    return seam


def overlay_seam(seam,image):
    for i,s in enumerate(seam):
        image[i,s] = [0,255,0]

    return image



def remove_vertical_seam(seam,img):
    rows,cols = img.shape[:2]

    for row in range(rows):
        for col in range(seam[row],cols-1): # no need to last we gona remove anyhow

            img[row,col]=img[row,col+1]

    
    img = img[:,0:cols-1]

    return img



## argument parsers

parsers = argparse.ArgumentParser(description="Seam Carving - Resize the image using Energy")
parsers.add_argument("-i","--image",metavar="",required=True,help="Location of image that you want to make small")
parsers.add_argument("-n","--number",type=int,metavar="",required=True,help="Enter Width you want to descrease: ")
parsers.add_argument("-v","--verbose",action='store_true',help="Show image shape after each decreament")
parsers.add_argument("-s","--save",action="store_true",help="Save the Seamed Image")
parsers.add_argument("-sh","--show",action="store_true",help="Show the low energy seam Image along with Seam image")
args = parsers.parse_args()



if __name__== "__main__":
   
    img = cv.imread(args.image)
    imgCopy = np.copy(img)
    energy = energyMatrix(img)


    for i in tqdm(range(args.number)):
        seam = find_vertical_seam(img,energy)
        img = remove_vertical_seam(seam,img)
        energy = energyMatrix(img)
        overlayImage = overlay_seam(seam,imgCopy)
        cv.imwrite("resized/resized-img/resized"+str(i)+args.image,img)
        cv.imwrite("resized/removed/removed"+str(i)+args.image,overlayImage)
        

    
    if args.verbose:
        print("Original Image shape : ",imgCopy.shape)
        print("Seamed Image shape : ",img.shape)

    if args.show:
        cv.imshow("image",img)
        cv.imshow("Layers removed",overlayImage)

    # if args.save:
    #     cv.imwrite("resized/resized"+args.image,img)
    #     cv.imwrite("resized/removed/removed"+args.image,overlayImage)

    cv.waitKey(0)
        