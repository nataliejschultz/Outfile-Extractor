#################################################################################################################################
################################ THIS PROGRAM ALLOWS YOU TO EXTRACT SPECIFIC DATA ###############################################
################################ FROM GAUSSIAN .OUT FILES, INCLUDING MULLIKEN,    ###############################################
################################ LOWDIN, NATURAL CHARGES, ATOM NUMBER, AND        ###############################################
################################ CHARGE UNIT TOTAL VALUE. JUST MODIFY MAIN_DIR    ###############################################
################################ TO BE THE GREATER DIRECTORY WHERE YOUR .OUT      ###############################################
################################ FILES ARE LOCATED.                               ###############################################
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
main_dir ="/Users/user/Desktop/single_test/"

#empty list of directories
directories = []

#universal booleans act as a switch to tell the program when to stop writing lines for a given section
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
print(directories)

#for loop takes definitions from previous loop to use them again in this new loop.

for item in directories:
    path = item["path"]
    jobname = item["jobname"]
    #creates an empty list of charges to append items to later. also reads lines from current output file to contents.
    charges = []
    #textfile is an empty list to put relevant lines of text into for each path.
    textfile=[]
    with open(path,"r") as file:
        contents = file.readlines()
        file.close()

    ### this for loop takes the number of atoms from the file and sets it as a float variable called numatoms
        for linenum, line in enumerate(contents):
            #empty list to append lines to


            #finds string in file
            if "NAtoms=   " in line:
                #splits line on space
                separate = line.split(" ")
                #temporary value is the fifth item in the split line
                temp = (separate[4])
                #numatoms is the number of atoms in the file.
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
                #universal boolean set to false once our desired section ends.
                data_mulliken = False

            #appends modified section to charges list
            if data_mulliken:
                new_line = format_line(line)
                joined_line = ",".join(new_line) + "\n"
                print(joined_line)
                charges.append(joined_line)

            #extracts lowdin charges in the same way as described above
            if "Lowdin Atomic Charges:" in line:
                data_lowdin = True
            if "Lowdin atomic charges with hydrogens summed" in line:
                data_lowdin = False

            if data_lowdin:
                new_line = format_line(line)
                joined_line = ",". join(new_line) +"\n"
                print(joined_line)
                charges.append(joined_line)

            #extracts natural charges in the same way as described above
            if "Natural  ---------" in line:
                data_natural = True

            if data_natural:
                new_line = format_natural_line(line)
                joined_line = ",". join(new_line) + "\n"
#                 print(joined_line)
                charges.append(joined_line)

            if "Natural Population" in line:
                data_natural = False

            #prints out total charge of the different units in the structure.
            if "Charge unit " in line:
                charges.append(line)

            #if charges exists and has data in it, open a new file in our original directory and write charges to it.
            if len(charges) > 0:
                temp_path = path.split("/")
                temp_path.pop(-1)
                newpath = "/".join(temp_path)
                with open(os.path.join(newpath, jobname +".csv"), "w") as csv:
#                     output_file = os.path.join(newpath, jobname + ".csv")
                    csv.writelines(charges)
                csv.close()

            #from here, the code is reading the same file but modifying sections for writing in a text file.

            if "Molecular unit" and "(NO3)" in line:
                unit_line=line.split()[2]
                ion_unit=float(unit_line)
                print("The Nitrate ion unit number is:", ion_unit)

            if "Second Order Perturbation Theory Analysis of Fock Matrix" in line:
                data_units = True

            if data_units and ("within unit" in line or "from unit" in line):
                if "None above threshold" not in contents[linenum + 1]:
                    unit_line = False
                    #for loop loops through the current line+1 to the end of the file, with one line subtracted to account
                    #for indexing
                    for i in range(linenum+1, len(contents)-1):
                        try:
                            #if the next line is empty, the for loop breaks and moves on to the next line.
                            if len(contents[i+1].split()) < 1:
                                break
                            energy_line = float(contents[i].split()[-3])
                            if energy_line > 10:
                                if unit_line == False:
                                    textfile.append(line)
                                    unit_line = True
                                textfile.append(contents[i])
    #                             textfile.append(energy_line)
                        except Exception:
                            pass
                    print("+++++")
                    print(textfile)


            if " Natural Bond Orbitals (Summary):" in line:
                data_units = False
                print (line)

                temp_path=path.split("/")
                temp_path.pop(-1)
                newpath="/".join(temp_path)
                with open(os.path.join(newpath, jobname+".txt"), "w") as txtfile:
                    text_file = os.path.join(newpath, jobname+".txt")
#                     print(f"output path: {text_file}")
                    txtfile.writelines(textfile)
                    txtfile.close()

print(f"output path: {output_file}")
print("the number of atoms in", jobname, "is", numatoms)
print("\n")
#

