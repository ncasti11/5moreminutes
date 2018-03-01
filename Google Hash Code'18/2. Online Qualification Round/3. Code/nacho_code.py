# --------------------------------------------------------
#           PYTHON PROGRAM
# Here is where we are going to define our set of...
# - Imports
# - Global Variables
# - Functions
# ...to achieve the functionality required.
# When executing > python 'this_file'.py in a terminal,
# the Python interpreter will load our program,
# but it will execute nothing yet.
# --------------------------------------------------------

import os
import codecs

# ------------------------------------------
# 1. FUNCTION parse_in
# ------------------------------------------
def parse_in(i_name):
    # 1. We create the output variable
    res = {}

    # 2. We open the file for reading
    my_input_file = codecs.open(i_name, "r", encoding='utf-8')

    # 3. We read the first line of the file
    res["num_rows"], res["num_columns"], res["min_ingredient"], res["max_cells"] = map(int, my_input_file.readline().strip().split())

    # 4. We read the rest of lines of the file

    # 4.1. We use a list of lists of boolean to represent the pizza content
    res["content"] = []

    # 4.2. We fill each row of the pizza
    for line in my_input_file:
        # 4.2.1. We remove the end of line from line
        line = line.replace("\n", "")

        # 4.2.2. So far the row is empty
        row = []

        # 4.2.3. We append the column to the row content
        for index in range(len(line)):
            if line[index] == 'M':
                row.append(True)
            else:
                row.append(False)

        # 4.2.4. We append the row to the pizza content
        res["content"].append(row)

    # 5. We close the file
    my_input_file.close()

    # 6. We return res
    return res

# ------------------------------------------
# 2. FUNCTION parse_out
# ------------------------------------------
def parse_out(o_name, res):
    # 1. We open the file for reading
    my_output_file = codecs.open(o_name, "w", encoding='utf-8')

    # 2. We write the number of slices used
    num_slices = res["num_slices"]
    my_output_file.write(str(num_slices) + "\n")

    # 3. We print all the slices
    for slice in res["slices"]:
        my_output_file.write(str(slice[0]) + " " + str(slice[1]) + " " + str(slice[2]) + " " + str(slice[3]) + "\n")

    # 4. We close the file
    my_output_file.close()

# ------------------------------------------
# 3.1. FUNCTION explore_row
# ------------------------------------------
def explore_row(row_content, num_columns, min_ingredient, max_cells, row_taken, row_index):
    # 1. We create the output_variable
    res = ()
    num_slices = 0
    slices = []

    # 1. We have starting index
    start_index = 0

    # 2. We compute the max starting index
    max_starting_index = num_columns - (2 * min_ingredient)

    # 3. We loop for all possibilities
    while (start_index <= max_starting_index):
        # 3.1. We get the end index
        end_index = min(num_columns - 1, (start_index + max_cells) - 1)

        # 3.2. We get the size of the range
        range_size = (end_index - start_index) + 1

        # 3.3. If the range is big enough, we try it
        if (range_size >= (2 * min_ingredient)):

            # 3.3.1. We get the content we are interested into
            candidates = row_content[start_index:(end_index+1)]

            # 3.3.2. We count the number of appearances of ingr1 in candidates
            ingr1_appearances = candidates.count(False)

            # 3.3.3. If the number of cells of both ingredients are enough, then we add the range as a slice of the solution
            if (ingr1_appearances >= min_ingredient) and \
               ((range_size - ingr1_appearances) >= min_ingredient):

                # 3.3.3.1. We increase the number of slices
                num_slices = num_slices + 1

                # 3.3.3.2. We add the slice coordinates
                slices.append([row_index, start_index, row_index, end_index])

                # 3.3.3.3. We mark all these positions as taken
                for c_index in range(start_index, (end_index+1)):
                    row_taken[c_index] = True

                # 3.3.3.4. We set start_index to end_index
                start_index = end_index

        # 3.4. We increase start_index
        start_index = start_index + 1

    # We assign res properly
    res = (num_slices, slices)

    # We return res
    return res

# ------------------------------------------
# 3. FUNCTION strategy
# ------------------------------------------
def strategy(input_info):
    # 1. We create the output variable
    res = {}
    res["num_slices"] = 0
    res["slices"] = []

    # 2. We traverse the pizza, marking all positions as non-taken
    taken = []
    for r in range(input_info["num_rows"]):
        # 2.1. So far the row is empty
        t = []

        # 2.2. We populate it as all non-taken
        for c in range(input_info["num_columns"]):
            t.append(False)

        # 2.3. We append the row to taken
        taken.append(t)

    # 3. We traverse the pizza by rows
    for row_index in range(input_info["num_rows"]):
        # 3.1. We append as many slices as possible from the row
        (new_num_slices, new_slices) = explore_row(input_info["content"][row_index],
                                                           input_info["num_columns"],
                                                           input_info["min_ingredient"],
                                                           input_info["max_cells"],
                                                           taken[row_index],
                                                           row_index)

        # 3.2. We add the result of the row to the overall solution
        res["num_slices"] = res["num_slices"] + new_num_slices

        for n_slice in new_slices:
            res["slices"].append(n_slice)

    # 4. We return res
    return res

# ------------------------------------------
# 4. FUNCTION solve_instance
# ------------------------------------------
def solve_instance(i_name, o_name):
    # 1. We do the parseIn from the input file
    input_info = parse_in(i_name)

    # 2. We do the strategy to solve the problem
    output_info = strategy(input_info)

    # 3. We do the parse out to the output file
    parse_out(o_name, output_info)

#------------------------------------------
# FUNCTION 5.1. get_parent_directory
#------------------------------------------
def get_parent_directory(d):
    # 1. We create the output variable
    res = ""

    # 2. We reverse the string representing the path
    rev = d[::-1]

    # 3. We look for the '\\' character representing the parent folder
    if "\\" in rev:
        # 3.1. If there is, we take all the name of the directory until the last '\\', which turns to be the first one when the
        # folder string name has been reversed.
        i = rev.index("\\")
        sub_rev = rev[(i+1):len(rev)]

        # 3.2. We reverse the parent folder again so as to make the string going forward once again
        res = sub_rev[::-1]
    # 4. If there is no parent directory, we just return d
    else:
        res = d
        print("No posible to go one directory up")

    # 5. We return the output variable
    return res

# ------------------------------------------
# 5. FUNCTION solve_benchmark
# ------------------------------------------
def solve_benchmark():
    # 1. Get the current directory
    c_dir = os.getcwd()

    # 2. Get the instances directory
    i_dir = get_parent_directory(c_dir) + "\\2. Instances"

    # 3. Get the list of instances
    instances = os.listdir(i_dir)

    # 4. We remove their extension
    for index in range(len(instances)):
        name = instances[index]
        name = name[:-3]
        instances[index] = name

    # 5. Get the solution directory
    s_dir = get_parent_directory(c_dir) + "\\4. Solutions"

    # 6. We solve the benchmark
    for name in instances:
        # 6.1. Get the full name of the input file
        i_name = i_dir + "\\" + name + ".in"
        o_name = s_dir + "\\" + name + ".out"

        # 6.2. We solve the instance
        solve_instance(i_name, o_name)

# ---------------------------------------------------------------
#           PYTHON EXECUTION
# This is the main entry point to the execution of our program.
# It provides a call to the 'main function' defined in our
# Python program, making the Python interpreter to trigger
# its execution.
# ---------------------------------------------------------------
if __name__ == '__main__':
    # 1. We set a variable for debug
    debug = False

    # 2. If we are debugging we solve the example instance
    if debug == True:
        i_name = "C://Users//Ignacio.Castineiras//Desktop//IEEE Society//6. Google Hash Code'18//2. Online Qualification Round//2. Instances//example.in"
        o_name = "C://Users//Ignacio.Castineiras//Desktop//IEEE Society//6. Google Hash Code'18//2. Online Qualification Round//4. Solutions//example.out"
        solve_instance(i_name, o_name)
    # 3. If we are ok, we solve the entire benchmark
    else:
        solve_benchmark()
