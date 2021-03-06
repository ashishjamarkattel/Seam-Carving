

# Seam-Carving

Technique to resized a images.One of the metrics that we can use is the value of the derivative at each point. This is a
good indicator of the level of activity in that neighborhood. If there is some activity, then
the pixel values will change rapidly. Hence the value of the derivative at that point would
be high. On the other hand, if the region were plain and uninteresting, then the pixel
values wouldn’t change as rapidly. So, the value of the derivative at that point in the
grayscale image would be low. This thing is called enegry matrix.
For each pixel location, we compute the energy by summing up the X and Y derivatives at
that point. We compute the derivatives by taking the difference between the current pixel
and its neighbors. There are various possible ways to achive this

    1. Develop a matrix that detect horizontal and vertical edges
    and combine together.

    2. Use Filter - Sobel that works on same principle.





## Demo

#### Removed Vertical-50 lines

![alt text](https://github.com/ashishjamarkattel/Seam-Carving/blob/master/gif/6cxuph.gif)

#### Resized in Time-stamp
![alt text](https://github.com/ashishjamarkattel/Seam-Carving/blob/master/gif/6cxurr.gif)



## Run Locally

Clone the project

```bash
  git clone https://github.com/ashishjamarkattel/Seam-Carving
```

Go to the project directory

```bash
  cd [your directory_name]
```

Install dependencies

```bash
  pip install numpy
  pip install opencv-python
  pip install tqdm
```

Resize Your image

```bash
  python carving.py -i [image-name] -n [number of vertical line to remove] -sh
```

Help
```bash
  python carving.py -h
```


### 

###


