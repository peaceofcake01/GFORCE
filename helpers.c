#include "helpers.h"
#include <math.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#define MIN(a,b) (((a)<(b))?(a):(b))
#define MAX(a,b) (((a)>(b))?(a):(b))


void swap(int *a, int *x);

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    float GrayS = 0;
    float x = 0;
    float y = 0;
    float z = 0;



    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            x = (image[i][j].rgbtRed);
            y = (image[i][j].rgbtGreen);
            z = (image[i][j].rgbtBlue);
            int offGrays = (int) roundf(GrayS);
            GrayS = (x + y + z) / 3;
            offGrays = roundf(GrayS);
            image[i][j].rgbtRed = offGrays;
            image[i][j].rgbtGreen = offGrays;
            image[i][j].rgbtBlue = offGrays;
        }
    }

}



// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
 {
    float x = 0;
    float y = 0;
    float z= 0;
    float sepiaRed = 0;
    float sepiaGreen = 0;
    float sepiaBlue = 0;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            x = image[i][j].rgbtRed;
            y = image[i][j].rgbtGreen;
            z = image[i][j].rgbtBlue;

            sepiaRed = .393 * x + .769 * y + .189 * z;
            sepiaGreen = .349 * x + .686 * y + .168 * z;
            sepiaBlue = .272 * x + .534 * y + .131 * z;

            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }

            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }

            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }
            int offsepiaRed = (int) roundf(sepiaRed);
            int offsepiaGreen = (int) roundf(sepiaGreen);
            int offsepiaBlue = (int) roundf(sepiaBlue);
            image[i][j].rgbtRed = round(offsepiaRed);
            image[i][j].rgbtGreen = round(offsepiaGreen);
            image[i][j].rgbtBlue = round(offsepiaBlue);
        }

    }
}


// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{

    int x = 0;
    int y = 0;
    int z = 0;
    int a = 0;
    int b = 0;
    int c = 0;

    RGBTRIPLE*s = malloc (height*sizeof(image[height])[width]);

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width/2; j++)
        {
            x = image[i][j].rgbtRed;
            y = image[i][j].rgbtGreen;
            z = image[i][j].rgbtBlue;

            a = image[i][width - j - 1].rgbtRed;
            b = image[i][width - j - 1].rgbtGreen;
            c = image[i][width - j - 1].rgbtBlue;


            image[i][width - j - 1].rgbtRed = x;
            image[i][width - j - 1].rgbtGreen = y;
            image[i][width - j - 1].rgbtBlue = z;

            image[i][j].rgbtRed = a;
            image[i][j].rgbtGreen = b;
            image[i][j].rgbtBlue = c;
        }

    }
}



// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    {
    RGBTRIPLE temp[height][width];
    int x = 0;
    int y = 0;
    int z = 0;
    int offx = 0;
    int offy = 0;
    int offz = 0;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {

            float sum_red = 0;
            float sum_green = 0;
            float sum_blue = 0;
            int counter = 0;
            for (int k = MAX(0, i-1); k < MIN(i + 2, height); k++)
               {


                for (int m = MAX(0, j-1); m < MIN(j+2, width); m++)
                    {
                        sum_red += image[k][m].rgbtRed;
                        sum_green += image[k][m].rgbtGreen;
                        sum_blue += image[k][m].rgbtBlue;
                        counter++;
                    }
               }




            float avg_red= sum_red / counter;
            float avg_green = sum_green / counter;
            float avg_blue = sum_blue / counter;

            printf("%f: avg=red\n", avg_red);


            int offavg_r = (int) roundf(avg_red);
            int offavg_g = (int) roundf(avg_green);
            int offavg_b = (int) roundf(avg_blue);

             printf("%i: offavg=red\n", offavg_r);



            temp[i][j].rgbtRed = offavg_r;
            temp[i][j].rgbtGreen = offavg_g;
            temp[i][j].rgbtBlue = offavg_b;

          }


    }

   for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = temp[i][j];
        }
    }
    }
}




 //if(i == 0 && j == 0)
//             {
//             offx=(image[i][j+1].rgbtRed + image [i-1][j].rgbtRed + image[i-1][j+1].rgbtRed)/3;
//             offy = (image[i][j+1].rgbtGreen + image [i-1][j].rgbtGreen + image[i-1][j+1].rgbtGreen)/3;
//             offz = (image[i][j+1].rgbtBlue + image [i-1][j].rgbtBlue + image[i-1][j+1].rgbtBlue)/3;
//             }

//             else if (i==0 && j == width - 1)
//             {
//             offx = (image[i][j-1].rgbtRed + image [i-1][j].rgbtRed + image[i-1][j-1].rgbtRed)/3;
//             offy = (image[i][j-1].rgbtGreen + image [i-1][j].rgbtGreen + image[i-1][j-1].rgbtGreen)/3;
//             offz = (image[i][j-1].rgbtBlue + image [i-1][j].rgbtBlue + image[i-1][j-1].rgbtBlue)/3;
//             }

//             else if (i==height - 1 && j == 0)
//             {
//             offx = (image[i+1][j+1].rgbtRed + image [i+1][j].rgbtRed + image[i][j+1].rgbtRed)/3;
//             offy = (image[i+1][j+1].rgbtGreen + image [i+1][j].rgbtGreen + image[i][j+1].rgbtGreen)/3;
//             offz = (image[i+1][j+1].rgbtBlue + image [i+1][j].rgbtBlue + image[i][j+1].rgbtBlue)/3;
//             }

//             else if (i==height - 1 && j == width - 1)
//             {
//             offx = (image[i-1][j-1].rgbtRed + image [i+1][j].rgbtRed + image[i][j - 1].rgbtRed)/3;
//             offy = (image[i-1][j-1].rgbtGreen + image [i+1][j].rgbtGreen + image[i][j - 1].rgbtGreen)/3;
//             offz = (image[i-1][j-1].rgbtBlue + image [i+1][j].rgbtBlue + image[i][j - 1].rgbtBlue)/3;
//             }


//             else if (i==0 && j != 0)
//             {


//             }
//             else if(i != 0 && j == width - 1)
//             {

//             }
//             else if (i==height - 1 && j != 0)
//             {

//             }
//             else if (i!=height - 1 && j == width - 1)
//             {

//             }
//             else
//             {
//             offx = (image[i-1][j-1].rgbtRed + image [i-1][j].rgbtRed + image[i-1][j+1].rgbtRed
//             + image [i][j-1].rgbtRed+ image[i][j].rgbtRed + image [i][j+1].rgbtRed
//             + image[i+1][j-1].rgbtRed + image [i+1][j].rgbtRed + image [i+1][j+1].rgbtRed)/9;

//             offy = (image[i-1][j-1].rgbtGreen + image [i-1][j].rgbtGreen + image[i-1][j+1].rgbtGreen
//             + image [i][j-1].rgbtGreen + image[i][j].rgbtGreen + image [i][j+1].rgbtGreen +
//             image[i+1][j-1].rgbtGreen + image [i+1][j].rgbtGreen + image [i+1][j+1].rgbtGreen)/9;

//             offz = (image[i-1][j-1].rgbtBlue + image [i-1][j].rgbtBlue + image[i-1][j+1].rgbtBlue
//             + image [i][j-1].rgbtBlue + image[i][j].rgbtBlue + image [i][j+1].rgbtBlue
//             + image[i+1][j-1].rgbtBlue + image [i+1][j].rgbtBlue + image [i+1][j+1].rgbtBlue)/9;
//             }

//             image[i][j].rgbtRed = offx;
//             image[i][j].rgbtGreen = offy;
//             image[i][j].rgbtBlue = offz;