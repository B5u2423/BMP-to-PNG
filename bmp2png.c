/*****************************************************
 * bmp2png -- convert bitmap image to png
 *
 * Usage:
 *      bmp2png <input_bmp> <output_png>
 *
 * Restrictions:
 *      No looping routine, no input sanitizing. All
 *  parameters regarding png output image must be tinkered
 *  by hand.
 *****************************************************/

#include <FreeImage.h>
#include <png.h>
#include <stdio.h>
#include <stdlib.h>

void bmp2png (char *bmpfile, char *pngfile);

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "Error: Invalid command syntax\n");
        fprintf(stderr, "Usage:\n");
        fprintf(stderr, "bmp2png <input_bmp> <output_png>\n");
        exit(8);
    }
    bmp2png(argv[1], argv[2]);
    return 0;
}


/*****************************************************
 * bmp2png -- convert an image from bmp to png using the
 *      FreeImage library.
 *****************************************************/

void bmp2png (char *bmpfile, char *pngfile) {
    // FreeImage init
    FreeImage_Initialise(TRUE);

    // load bmp
    FIBITMAP* bmpSource = FreeImage_Load(FIF_BMP, bmpfile, BMP_DEFAULT);
    int width = FreeImage_GetWidth(bmpSource);
    int height = FreeImage_GetHeight(bmpSource);

    // convert bmp to 24 bits BGR
    FIBITMAP* bgrImage = FreeImage_ConvertTo24Bits(bmpSource);
    // unload bitmap
    FreeImage_Unload(bmpSource);

    // manually swap BGR to RGB
    for (int y = 0; y < height; ++y) {
        for (int x = 0; x < width; ++x) {
            RGBQUAD pixel;
            FreeImage_GetPixelColor(bgrImage, x, y, &pixel);

            BYTE temp = pixel.rgbRed;
            pixel.rgbRed = pixel.rgbBlue;
            pixel.rgbBlue = temp;

            FreeImage_SetPixelColor(bgrImage, x, y, &pixel);
        }
    }
    // invert the image
    FreeImage_FlipVertical(bgrImage);

    // initialize libpng
    png_structp png = png_create_write_struct(PNG_LIBPNG_VER_STRING, NULL, NULL, NULL);
    png_infop info = png_create_info_struct(png);

    // writing png
    FILE* pngFile = fopen(pngfile, "wb");
    png_init_io(png, pngFile);

    // PNG header info
    png_set_IHDR(
        png,
        info,
        width,
        height,
        8,  // bit depth
        PNG_COLOR_TYPE_RGB,
        PNG_INTERLACE_NONE,  // disable interlacing here
        PNG_COMPRESSION_TYPE_DEFAULT,
        PNG_FILTER_TYPE_DEFAULT
    );
         
    // setting parameters for comparison
    png_set_compression_strategy(png, 0);
    png_set_text_compression_level(png, 6);
    png_set_compression_mem_level(png, 9);

    // start writing
    png_write_info(png, info);

    // get pointer to bitmap image data
    // at offset 54
    BYTE* imageData = FreeImage_GetBits(bgrImage);
    for (int y = 0; y < height; ++y) {
        png_write_row(png, imageData + y * FreeImage_GetPitch(bgrImage));
    }

    // stop writing
    png_write_end(png, NULL);

    // clean up
    png_destroy_write_struct(&png, &info);
    fclose(pngFile);
    FreeImage_Unload(bgrImage);
    FreeImage_DeInitialise();
}
