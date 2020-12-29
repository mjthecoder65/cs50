#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

int main(int argc, char *argv[])
{
    // Ensure the user enter a correct input
    const int BUFFERSIZE = 512;
    unsigned char buffer[BUFFERSIZE];

    // Inform user if enters input in a wrong way.
    if (argc == 1)
    {
        printf("Usage: %s image\n", argv[0]);
    }

    // Open a file
    FILE *photo_file = fopen(argv[1], "r");

    if (photo_file == NULL)
    {
        printf("Sorry, couldn't open the image file! Try again.");
        return 1;
    }

    FILE *photo = NULL;
    int  is_jpg_found = 0;
    int file_count = 0;
    while (fread(buffer, BUFFERSIZE, 1, photo_file) == 1)
    {
        // Checking if the found the 512 read block is jpeg
        if (buffer[0] == 0xff &&  buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[0] & 0xe0) == 0xe0)
        {
            // If the photo was found close the previous output file.
            if (is_jpg_found == 1)
            {
                fclose(photo);
            }
            else
            {
                is_jpg_found = 1;
            }
            // Declaring and rename the output file
            char filename[8];
            sprintf(filename, "%03d.jpg", file_count);
            photo = fopen(filename, "a");
            file_count++;

        }
        // Write to the file if the image is found
        if (is_jpg_found == 1)
        {
            fwrite(&buffer, BUFFERSIZE, 1, photo);
        }

    }
    // closing input streams to avoid memory leak
    fclose(photo_file);
    fclose(photo);
    return 0;
}
