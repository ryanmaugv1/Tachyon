//
//  Tachus
//  lexer.c
//
//  Created on 26/05/17
//  Ryan Maugin <ryan.maugin@adacollege.org.uk>
//

#include <iostream>
#include <fstream>
#include <string>
using namespace std;

// Function Declration
string openSourceFile();


int main () {

    string data = openSourceFile();

    return 0;
}


/**
 * Open Source File
 * This will open the source file and save it's content
 * @return fileContent
 */
string openSourceFile () {
    ifstream sourceFile("./src/test.txt"); // Open file
    string sourceFileLine;
    string fileContent;

    // Loop through each line and store it in fileContent
    while ( sourceFile.good() ) {
        getline(sourceFile, sourceFileLine);
        // if sourceFileLine is empty then don't save it
        if (sourceFileLine != "") fileContent += sourceFileLine + "\n";
    }

    sourceFile.close(); // Close file
    return fileContent;
}
