import csv
import re
import matplotlib.pyplot as plt
from difflib import SequenceMatcher
from string import punctuation

clk_1_size = 0
clk_2_size = 0
first_clk_2 = 0


# Script clean receives a path to a script.txt file
# The function cleans the script of all words that are not - who spoke them or what they said
# e.g: background sounds or behavioral expressions
def script_clean(path, spc_to_speaker, spc_to_sent):
    clean_txt = open("clean_script.txt", "w")
    with open(path, "r") as txt_file:
        line = txt_file.readline()
        while line:
            # print ("Leading spaces", len(line) - len(line.lstrip(' ')))
            ws_count = len(line) - len(line.lstrip(' '))  # This calculated the number of preceeding whitespaces in each line
            if ws_count == spc_to_sent or ws_count == spc_to_speaker:  # Checking if the number of whitespaces is
                clean_txt.write(line)                                 # either spc_to_speaker or spc_to_sent which represent the name and sentance said
            line = txt_file.readline()

    with open("clean_script.txt", "r") as f:  # Cleaning the script from any instances of parentheses
        input = f.read()                      # using REGEX that goes through the entire file
        output = re.sub("[\(\[].[\s\S]*?[\)\]]", "", input)
        clean_txt1 = open("clean_script.txt", "w")
        clean_txt1.write(output)


# csv_twoClk receives the clean_script.txt it then creates a new CSV file
# that contains two columns - Name of speaker and how many words they said in a sentence
# i.e: Shrek, 8
def csv_two_clks(path, ws_speaker, ws_sentence):
    csv_file = open('mycsv.csv', 'w', newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Name', 'Num of words'])
    tmp_name = ""

    with open(path, "r") as txt_file:
        line = txt_file.readline()
        #ws_count = 0
        #num_of_words = 0
        while line:
            if not line.strip():  # Checking if line is not empty
                line = txt_file.readline()
                continue
            ws_count = len(line) - len(line.lstrip(' '))
            if ws_count == ws_speaker:   # If line has spc_to_speaker spaces then it represents a speaker name
                tmp_name = line.strip()  # saving the last speakers name so that we can insert it to the CSV file
                num_of_words = 0
            if ws_count == ws_sentence:
                num_of_words = len((line.strip()).split()) # If line has spc_to_sent spaces then it represents the sentence said
                csv_writer.writerow([tmp_name, num_of_words])
            line = txt_file.readline()


# extract_clks: receives a regular csv file and creates a new csv file
# which its columns represent our 2 un-normalised clocks = clks.csv
def extract_clks(path):
    clks_csv = open('clks.csv', 'w', newline='')
    csv_file = open(path, 'r')
    csv_reader = csv.reader(csv_file)
    csv_writer = csv.writer(clks_csv)

    csv_writer.writerow(['Clock 1', 'Clock 2'])

    name_tmp = ""
    name_count = -1
    words_count = 0

    next(csv_reader)  # This is used to skip the column titles

    for line in csv_reader:
        if name_count == -1:      # first 2 ifs are used to initialise the counters
            name_tmp = line[0]
            name_count += 1
        if words_count == 0:
            words_count = int(line[1])
            continue
        if line[0] == name_tmp:   # This means the speaker hasn't changed then we continue summing the words said
            words_count += int(line[1])
        else:
            csv_writer.writerow([name_count, words_count])  # Writing the data to the new CSV
            name_tmp = line[0]     # This is the next speakers name
            words_count += int(line[1])
            name_count += 1


# This function receives a path to the CSV file that contains the two clocks C1 & C2
# and creates a new CSV file that contains the normalized clocks: N(C1) & N(C2)
# and their difference in column 3 (Clock1 - Clock2) that will be needed later
def normal_clks(path):

    global clk_1_size
    global clk_2_size
    global first_clk_2

    n_clks_csv = open('n_clks.csv', 'w', newline='')
    csv_file = open(path, 'r')
    csv_reader = csv.reader(csv_file)
    csv_writer = csv.writer(n_clks_csv)

    csv_writer.writerow(['Normal Clock 1', 'Normal Clock 2', 'Clk_1 - Clk_2'])

    for line in csv_reader:
        pass

    clk_1_size = int(line[0])
    clk_2_size = int(line[1])

    csv_file = open(path, 'r')
    csv_reader = csv.reader(csv_file)

    next(csv_reader)
    flag = 0
    for line in csv_reader:  # In this loop we normalize the clocks using the formula to make sure the clocks are now in
        if flag == 0:        # the interval of [0,1]
            first_clk_2 = int(line[1])
            flag = 1
        csv_writer.writerow([int(line[0])/clk_1_size, (int(line[1]) - first_clk_2)/(clk_2_size - first_clk_2),
                             (int(line[0])/clk_1_size) - ((int(line[1]) - first_clk_2)/(clk_2_size - first_clk_2))])


# Graph plot for N(Clk1) and N(Clk1-Clk2)
def graph_plot(path):
    csv_file = open(path, 'r')
    csv_reader = csv.reader(csv_file)
    x = []
    y = []
    next(csv_reader)

    for line in csv_reader:
        x.append(float(line[0]))
        y.append(float(line[2]))

    y_max = max(y)
    y_min = min(y)

    plt.plot(x, y, color='blue', linestyle='-', linewidth=3,
             markerfacecolor='blue', markersize=12)
    plt.ylim(y_min-0.01, y_max+0.01)
    plt.xlim(0, 1)
    plt.xlabel('Speaker Change')
    plt.ylabel('Difference between Clk1 and Clk2 ')
    plt.title('Graph')
    plt.show()


# Here we clean the subtitles of the movie from all parentheses using a REGEX
def clean_subtitles(path):
    with open(path, "r") as f:  # Cleaning the subtitles from any instances of parentheses
        input = f.read()        # using REGEX that goes through the entire file
        output = re.sub("[\(\[</].[\s\S]*?[\>\)\]]", "", input)
        clean_txt1 = open("clean_subtitles.txt", "w")
        clean_txt1.write(output)


# This function receives the normal_clks and applies math to find critical word
def finding_norm_critical_word(path):
    csv_file = open(path, 'r')
    csv_reader = csv.reader(csv_file)


#Function receives normal_speaker_change and returns normal_word_count
def extract_normal_word(normal_critical_speaker, path):
    csv_file = open(path, 'r')
    csv_reader = csv.reader(csv_file)
    next(csv_reader)
    for line in csv_reader:
        if float(line[0]) == normal_critical_speaker:
            return float(line[1])


# This function gets the normal critical word and returns their timestamp
def finding_ts(normal_critical_word, path):
    global clk_2_size
    global first_clk_2

    # This is how we extract the word number
    critical_word = (normal_critical_word * clk_2_size) + first_clk_2
    print("Critical word number is", critical_word)
    with open(path, "r") as txt_file:
        line = txt_file.readline()
        word_count = 0
        tmp_ts = ''
        while line:
            if not line[0].isdigit():
                word_count += len((line.strip()).split())
                if word_count >= critical_word:
                    return tmp_ts
            if line[0] == '0':
                tmp_ts = line
            line = txt_file.readline()


# Checking the similarity between the SRT file and script file
def similarity_srt_script(srt_path, script_path, space_to_name):
    with open(srt_path, "r") as f:
        tmp_txt = open("tmp_srt.txt", "w")
        input = f.read()
        output = "".join(c for c in input if c not in punctuation)
        tmp_txt.write(output)

    with open(script_path, "r") as f:
        tmp_txt = open("tmp_script.txt", "w")
        input = f.read()
        output = "".join(c for c in input if c not in punctuation)
        tmp_txt.write(output)

    with open('tmp_script.txt', "r") as f:
        tmp_txt = open("no_name_script.txt", "w")
        line = f.readline()
        while line:
            ws_count = len(line) - len(line.lstrip(' '))
            if ws_count != space_to_name:
                tmp_txt.write(line)
            line = f.readline()











