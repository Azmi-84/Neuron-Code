#include <stdio.h>
/*
There are two types of file:
1. Text File
2. Binary File

In text file each file each line end with character '\n'
It can be read or written by any text editor
They are generally stored with .txt file extension
Text file can also be used to store the source code

The binary files can be created only from within a program and their contents can only be read by a program
More secure as they are not ealisy readable
Stored as .bin extension

A file pointer is a reference to a particular position in the opened file. It is used in file handling to perform all file operations such as read, write, close, etc. We use the FILE macro to declare the file pointer variable. The FILE macro is defined inside <stdio.h> header file.

Syntax of File Pointer

FILE* pointer_name;
*/

int main()
{
    char filename = 'main.txt';
    FILE *fptr;
    return 0;
}