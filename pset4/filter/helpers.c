#include "helpers.h"
#include <math.h>
// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            RGBTRIPLE pixel = image[i][j];
            int average = round((pixel.rgbtRed + pixel.rgbtGreen + pixel.rgbtBlue) / 3.0);
            image[i][j].rgbtRed =  image[i][j].rgbtGreen =  image[i][j].rgbtBlue = average;
        }
    }
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    int sepiaRed, sepiaBlue, sepiaGreen;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            sepiaRed = round(0.393 * image[i][j].rgbtRed + 0.769 * image[i][j].rgbtGreen + 0.189 * image[i][j].rgbtBlue);
            sepiaGreen = round(0.349 * image[i][j].rgbtRed + 0.686 * image[i][j].rgbtGreen + 0.168 * image[i][j].rgbtBlue);
            sepiaBlue = round(0.272 * image[i][j].rgbtRed + 0.534 * image[i][j].rgbtGreen + 0.131 * image[i][j].rgbtBlue);

            image[i][j].rgbtRed = sepiaRed > 255 ? 255 : sepiaRed;
            image[i][j].rgbtGreen = sepiaGreen > 255 ? 255 : sepiaGreen;
            image[i][j].rgbtBlue = sepiaBlue > 255 ? 255 : sepiaBlue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int left = j, right = width - j - 1;
            if (left < right)
            {
                temp = image[i][left];
                image[i][left] = image[i][right];
                image[i][right] = temp;
            }
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];
    // Compying the image to the temporary container
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            temp[i][j] = image[i][j];
        }
    }

    // blurring the image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int total_blue;
            int total_green;
            int total_red;
            float count;
            total_blue = total_green = total_red = count = 0;

            // Checking middle pixel
            if (i >= 0 && j >= 0)
            {
                total_red += temp[i][j].rgbtRed;
                total_green += temp[i][j].rgbtGreen;
                total_blue += temp[i][j].rgbtBlue;
                count++;
            }
            // Checking left pixel
            if (i >= 0 && j - 1 >= 0)
            {
                total_red += temp[i][j - 1].rgbtRed;
                total_green += temp[i][j - 1].rgbtGreen;
                total_blue += temp[i][j - 1].rgbtBlue;
                count++;
            }
            //Checking top pixel
            if (i - 1 >= 0 && j >= 0)
            {
                total_red += temp[i - 1][j].rgbtRed;
                total_green += temp[i - 1][j].rgbtGreen;
                total_blue += temp[i - 1][j].rgbtBlue;
                count++;
            }
            // Checking pixel on the top left corner
            if (i - 1 >= 0 && j - 1 >= 0)
            {
                total_red += temp[i - 1][j - 1].rgbtRed;
                total_green += temp[i - 1][j - 1].rgbtGreen;
                total_blue += temp[i - 1][j - 1].rgbtBlue;
                count++;
            }
            // Checking pixel on the right corner
            if ((i >= 0 && j + 1 >= 0) && (i >= 0 && j + 1 < width))
            {
                total_red += temp[i][j + 1].rgbtRed;
                total_green += temp[i][j + 1].rgbtGreen;
                total_blue += temp[i][j + 1].rgbtBlue;
                count++;
            }
            // Checking pixel on the top right corner
            if ((i - 1 >= 0 && j + 1 >= 0) && (i - 1 >= 0 && j + 1 < width))
            {
                total_red += temp[i - 1][j + 1].rgbtRed;
                total_green += temp[i - 1][j + 1].rgbtGreen;
                total_blue += temp[i - 1][j + 1].rgbtBlue;
                count++;
            }
            // Checking pixel on the bottom
            if ((i + 1 >= 0 && j >= 0) && (i + 1 < height && j >= 0))
            {
                total_red += temp[i + 1][j].rgbtRed;
                total_green += temp[i + 1][j].rgbtGreen;
                total_blue += temp[i + 1][j].rgbtBlue;
                count++;
            }
            // Checking pixel on the bottom left corner
            if ((i + 1 >= 0 && j - 1 >= 0) && (i + 1 < height && j - 1 >= 0))
            {
                total_red += temp[i + 1][j - 1].rgbtRed;
                total_green += temp[i + 1][j - 1].rgbtGreen;
                total_blue += temp[i + 1][j - 1].rgbtBlue;
                count++;
            }

            // Checking Bottom right pixel
            if ((i + 1 >= 0 && j + 1 >= 0) && (i + 1 < height && j + 1 < width))
            {
                total_red += temp[i + 1][j + 1].rgbtRed;
                total_green += temp[i + 1][j + 1].rgbtGreen;
                total_blue += temp[i + 1][j + 1].rgbtBlue;
                count++;
            }
            // find average colour value
            image[i][j].rgbtRed = round(total_red / (float)count);
            image[i][j].rgbtGreen = round(total_green / (float)count);
            image[i][j].rgbtBlue = round(total_blue / (float)count);
        }
    }
    
    return;
}