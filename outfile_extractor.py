#################################################################################################################################
################################ THIS PROGRAM ALLOWS YOU TO EXTRACT SPECIFIC DATA ###############################################
################################ FROM GAUSSIAN .OUT FILES, INCLUDING MULLIKEN,    ###############################################
################################ LOWDIN, NATURAL CHARGES, ATOM NUMBER,            ###############################################
################################ CHARGE UNIT TOTAL VALUE, AND INTERACTIONS BETWEEN     ###############################################
################################ MOLECULE UNITS. JUST MODIFY MAIN_DIR TO BE THE       ###############################################
################################ GREATER DIRECTORY WHERE YOUR .OUTFILES ARE LOCATED.  ###############################################
############################### Author: Natalie Schultz                              ###############################################
#################################################################################################################################
import os

def format_line(line):
    """
    Formats lines of Mulliken and Lowdin charge section to export to csv
    params: line from the output file
    return: comma separated line for csv
    """
    #splits line using split function
    split_line=line.split()
    return split_line


def format_natural_line(line):
    """
    Formats the natural charge section of the output file for export to csv
    params: line from output file
    return: comma separated line for csv with irrelevant information excluded
    """
    #splits line using split function
    split_line = line.split()
    return split_line[0:3]

#directory where the nbo output "nbo.out" files are
main_dir ="/Users/user/Desktop/pythonfolder/git_projects/final_project/CHEM5630"

#empty list of directories
directories = []

#three universal booleans act as a switch to tell the program when to stop writing lines for a given section
data_mulliken = False
data_lowdin = False
data_natural = False

#for loop uses os.walk function to append the path to all desired nbo.out files.
for directory, full_path, filenames in os.walk(main_dir):
    for outfile in filenames:
        if "nbo.out" in outfile:
            outfile_path = os.path.join(directory, outfile)
            #basename function gives the name of the exact file that os.walk identified.
            x = os.path.basename(outfile)
            print("Found filename",x)
            #jobname is the first half of the filename when it's split on the period.
            jobname = x.split(".")[0]
            #the paths to each nbo.out file is appended to  a list called directories.
            directories.append({"path": outfile_path, "jobname": jobname})

#for loop takes definitions from previous loop to use them again in this new loop.
for item in directories:
    #grabs value of path from directories to be used later.
    path = item["path"]
    #grabs value of jobname from directories to be used later.
    jobname = item["jobname"]
    #creates an empty list of charges to append items to later.
    charges = []
    #textfile is an empty list to put relevant lines of text into for each path.
    textfile=[]
    # reads lines from current output file to temporary list called contents.
    with open(path,"r") as file:
        contents = file.readlines()
        file.close()
        #boolean value used as a switch for when to modify specific lines of contents
        data_units = False
        #empty string to append the number of atoms to.
        numatoms = ''

    ### this for loop takes the number of atoms from the file and sets it as a float variable called numatoms
        for linenum, line in enumerate(contents):

            #finds string in file
            if "NAtoms=" in line:
                #splits line on space
                separate = line.split(" ")
                #temporary value is the fourth item in the split line
                temp = (separate[3])
                #numatoms is the number of atoms in the file, modified as a float.
                numatoms = float(temp)


#this section extracts mulliken, lowdin,and natural charges using the functions above, and appends
#the modified lines to the charges list. natural charge has a slightly different format than mulliken
#and lowdin, so it uses a different function.

            #modifies and extracts mulliken charges:
            if "Mulliken charges:" in line:
                #after finding relevant string, sets universal boolean "data mulliken" to true.
                #this flag allows the code to stop when it finds a string that ends our desired section.
                data_mulliken = True
                charges.append(jobname)
                print("Mulliken is true")

            #string that ends the section we want to extract
            if "Sum of Mulliken charges" in line:
                charges.append(line)
                #boolean set to false once our desired section ends.
                data_mulliken = False

            #when our boolean is true:
            if data_mulliken:
                #new_line calls the format_line function.
                new_line = format_line(line)
                #joined_line modifies the new line to format properly for a csv file.
                joined_line = ",".join(new_line) + "\n"
                #appends properly formatted line to charges list
                charges.append(joined_line)

            #extracts lowdin charges in the same way as described above
            if "Lowdin Atomic Charges:" in line:
                #boolean set to true so that the correct section of code is operated on.
                data_lowdin = True
            if "Lowdin atomic charges with hydrogens summed" in line:
                #boolean set to false so that the correct section of code is operated on.
                data_lowdin = False

                #when our boolean is true:
            if data_lowdin:
                #calls the format_line function
                new_line = format_line(line)
                #modifies the new line properly for a csv.
                joined_line = ",". join(new_line) +"\n"
                #appends line to charges.
                charges.append(joined_line)

            #extracts natural charges in the same way as described above
            if "Natural  ---------" in line:
                #boolean set to true so that the correct section of code is operated on.
                data_natural = True

            if data_natural:
                #if boolean true, calls format_natural_line function to modify the line.
                new_line = format_natural_line(line)
                #formats line for writing to csv.
                joined_line = ",". join(new_line) + "\n"
#                #appends line.
                charges.append(joined_line)

                #sets boolean to false so that the correct section of code is operated on.
            if "Natural Population" in line:
                data_natural = False

            #appends the total charge of the different units in the structure to charges.
            if "Charge unit " in line:
                charges.append(line)

            #if charges has data in it...
            if len(charges) > 0:
                #we create a temporary path using the orginal nbo.out file path, splitting along "/"
                temp_path = path.split("/")
                #last element of the temp path is removed.
                temp_path.pop(-1)
                #new path joins our modified path on slashes, to give the file directory.
                newpath = "/".join(temp_path)
                #use our new path to open new file (jobname.csv) in the correct directory.
                with open(os.path.join(newpath, jobname +".csv"), "w") as csv:
                    #sets output_file to be printed at the end of the program.
                    output_file = os.path.join(newpath, jobname + ".csv")
                    #writes to the file!
                    csv.writelines(charges)
                csv.close()

            #from here, the code is reading the same file but modifying sections for writing in a text file.

            #finds a very specific line
            if "Molecular unit" and "(NO3)" in line:
                #takes the line and splits it, and grabs the third value
                unit_line=line.split()[2]
                #converts the unit_line from above and converts to a float
                ion_unit=float(unit_line)
                #print statement in the terminal so that user can compare with output files.
                print("The Nitrate ion unit number is:", ion_unit)

            if "Second Order Perturbation Theory Analysis of Fock Matrix" in line:
                #boolean set to true on this line. Used as a flag, just like it was above.
                data_units = True

                #finds if two specific strings are in a line to operate on them
            if data_units and ("within unit" in line or "from unit" in line):
                #excludes lines whose NEXT LINE (linenum+1) has "None above threshold" in it. This removes
                #any units that did not have significant interactions.
                if "None above threshold" not in contents[linenum + 1]:
                    #unit_line_appended boolean tells us if the "within unit" or "from unit" line has been appended yet.
                    #if false, we append it below
                    unit_line_appended = False

                    #for loop loops over the current line+1 to the end of the file, with one line subtracted to account
                    #for indexing
                    for i in range(linenum+1, len(contents)-1):
                        #try statement looks to see if the -3rd element of the line can
                        #be converted to a float. If it can, it is in our desired section of code.
                        try:
                            #if the next line is empty, the for loop breaks and skips on to the next line.
                            if len(contents[i+1].split()) < 1:
                                break
                                #if the current line's (contents[i]) third to last element is a float,
                                #the number is set to energy_line
                            energy_line = float(contents[i].split()[-3])
                            #if the value above is greater than 10....
                            if energy_line > 10:
                                #...AND if we haven't already appended the within unit/from unit line,
                                #the within/from unit line is appended to textfile. This is to account for
                                #unit interactions that have multiple interactions with an energy above 10,
                                #without re-appending the within/from unit line multiple times.
                                if unit_line_appended == False:
                                    textfile.append(line)
                                    #once that line is appended, the boolean is set to true for the next line.
                                    #we can now successfully append the current line in contents without
                                    #repeating the within/from unit line.
                                    unit_line_appended = True
                                #finally, the current content line is appended to textfile.
                                textfile.append(contents[i])

                            #except part of  try...except statement catches lines
                            #that failed the criteria of the try block. Mostly, lines that couldn't be converted to a float.
                            # It will pass these lines.
                        except Exception:
                            pass


            if " Natural Bond Orbitals (Summary):" in line:
                #the string above ends the desired section, so we set our boolean to false.
                data_units = False

                #once we have our lines in textfile, we want to write to a file.
                #temp path sets a temporary path that splits the original path of the output file on a "/".
                temp_path=path.split("/")
                #pop function removes the last item from the temp path, i.e. the actual nbo.out file name.
                temp_path.pop(-1)
                #new path joins temp path along slashes, to give us the directory of the nbo.out file.
                newpath="/".join(temp_path)
                #opens a new file at our directory, and titles it with the jobname.txt.
                with open(os.path.join(newpath, jobname+".txt"), "w") as txtfile:
                    #text_file set equal to the path for the print statement at the bottom.
                    text_file = os.path.join(newpath, jobname+".txt")
                    #writes to the text file!
                    txtfile.writelines(textfile)
                    #closes file.
                    txtfile.close()
#these print statements will show up in the terminal. It shows where outputs go, as well as number of atoms in the model.
print(f"csv output path: {output_file}")
print(f"textfile output path: {text_file}")
print("the number of atoms in", jobname, "is", numatoms)
#

