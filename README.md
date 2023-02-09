# CHEM5630 - Programming for Data Analysis in the Physical Sciences

## Overview
* This program takes a output file from gaussian after it has run NBO analysis (called our nbo.out file) on an optimized molecular model.  It can be run in terminal using `python outfile_extractor.py`. It will output two files to the directory of the original nbo.out file: a text file and a csv. It will also output print statements regarding the number of atoms in the model, as well as which unit of the model belongs to our ion (in this case, nitrate.)

## Explanation of files in repository
* outfile_extractor.py
  * This is the python file used to extract data from the nbo.out file.
  Command line is not needed to run this program, but the variable "main_dir" on line 34 needs to be changed to be the exact path where the n5_no3_nbo.out file is located (ex: if the path to n5_no3_nbo.out is in Users/home/n5_no3_nbo.out, then "main_dir" should be set equal to "Users/home/")
* n5_no3_nbo.out
  * The file we are reading and extracting data from. This file was originally generated
  as part of my research. The file was generated using gaussian on a quantum model that I
  created in avogadro/VMD.
* n5_no3_nbo_example.txt
  * This outputted text file lists the interactions between units of the molecular model. It only lists interactions that have an energy value greater than 10kcal/mol. This is very useful when trying to find orbitals that
  may take part in charge transfer.
* n5_no3_nbo_example.csv
  * This outputted csv extracts the Mulliken, Lowdin, and Natural charge of each atom in the model. It
  also lists the overall of each type of charge. At the bottom, the total charge of each unit is listed.
