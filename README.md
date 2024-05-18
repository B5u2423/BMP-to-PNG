<a id="readme-top"></a>

# BMP-to-PNG

## About 

Bài tập lớn Mã hóa Dữ liệu đa phương tiện. There are two programs: the one written in C convert .BMP image to .PNG. The Python program compare the PSNR between 2 different PNGs.

## Built With

This project is built with all the following frameworks/libraries/plugins:

* [FreeImage](https://freeimage.sourceforge.io/) 
* [OpenCV](https://pypi.org/project/opencv-python/)
* [PyQt5](https://pypi.org/project/PyQt5/)
* [NumPy](https://numpy.org/)

## Getting Started

To get a local copy up and running, please follow these simple steps. 

### Prerequisites

You MUST install all the libraries and packages before running either of the programs.

Install Free Image:

```bash
sudo apt-get install libfreeimage3 libfreeimage-dev
```

Install all the packages for Python program:

```bash
pip install -r requirement.txt
```

### Installing

Clone the repo

```bash
git clone https://github.com/B5u2423/BMP-to-PNG.git
```

`cd` into the cloned directory. Run the Makefile to compile the C converter program (Make sure to install all the dependencies in *Prerequisites* section)

```bash
make
```

## Deployment

Run the C program using the prompt to convert bitmap image. 

```bash
bmp2png <input_bmp> <output_png>
```

The parameters that affect PNG output quality must be manually configure in the source file and recompile. I just wanted a working program ASAP so I have to cut corners. As for the Python program, just simply run it, it has a GUI made with PyQt5 so it would be easier to navigate around.

![Python Program Preview](/assets/py-program-demo.png)

*Python Program preview*

<p align="right">(<a href="#readme-top">back to top</a>)</p>
