import csv
import re
import matplotlib.pyplot as plt
from difflib import SequenceMatcher
from string import punctuation
from heapq import nlargest
from heapq import nsmallest

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
            ws_count = len(line) - len(line.lstrip(' '))
            if ws_count == spc_to_sent or ws_count == spc_to_speaker:
                clean_txt.write(line)
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
                num_of_words = len((line.strip()).split())
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


# Function for derivative of normal Clocks so we can find critical moments
# derivative[i] = (clk_1-clk_2)[i]-((clk_1-clk_2)[i+1]
# We also find the 3 largest and the 3 smallest derivatives for timestamps
def derivative_and_find_index(path, num_of_max, num_of_min):
    elements = []
    derivative_list = []
    #max_value = [None] * num_of_max
    #min_value = [None] * num_of_min

    csv_file = open(path, 'r')
    csv_reader = csv.reader(csv_file)

    next(csv_reader)

    for line in csv_reader:
        elements.append(float(line[2]))

    for x in range(len(elements)):
        try:
            deriv = elements[x] - elements[x+1]
            derivative_list.append(deriv)
        except IndexError:
            break

    min_max_index = []

    count = 0
    #  This finds the all the min/max points in the graph and adds them to min_max_index
    for k in derivative_list:
        try:
            if k < 0 and derivative_list[count+1] > 0:  # This is a minimum point
                min_max_index.append(count)
                count += 1

            if k > 0 and derivative_list[count+1] < 0:  # This is a maximum point
                min_max_index.append(count)
                count += 1
            else:
                count += 1
        except IndexError:
            break

    min_max_value = []

    #  This takes the min_max_index and finds their corresponding Y value
    for n in min_max_index:
        min_max_value.append(float(elements[n]))

    max_values = nlargest(num_of_max, min_max_value)
    min_values = nsmallest(num_of_min, min_max_value)

    normal_critical_word_index = []
    count = 0
    for i in elements:
        if i in max_values or i in min_values:
            normal_critical_word_index.append(count)
            count += 1
        else:
            count += 1

    normal_critical_word_list = []
    csv_file = open(path, 'r')
    reader = csv.reader(csv_file)

    count = 0
    for line in reader:
        if count in normal_critical_word_index:
            normal_critical_word_list.append(float(line[1]))
            count += 1
        else:
            count += 1
    return normal_critical_word_list


# This function receives the critical word list and searches for a match between the script
# and SRT using sequence matching of the words
# and returns a list containing the indexes of the words in the SRT file
def find_word_index_with_matching_sequences(normal_word_list, script_path, srt_path):
    global clk_2_size
    global first_clk_2
    actual_critical_words = []

    # This is how we extract the word number
    for word in normal_word_list:
        actual_critical_words.append(int((word * clk_2_size) + first_clk_2))

    script_seq_list = []  # List of lists

    with open(script_path, "r") as script:
        script_data = script.read().replace('\x00', '')
        splitted_script = script_data.split()

        for word in actual_critical_words:
            script_seq = [splitted_script[word-2] + " " + splitted_script[word-1] + " " + splitted_script[word]
                          + " " + splitted_script[word+1] + " " + splitted_script[word+2]]
            script_seq_list.append(script_seq)

        print(script_seq_list)

    with open(srt_path, "r") as srt:
        srt_data = srt.read()
        splitted_srt = srt_data.split()
        count_1 = 0
        srt_sentence_index = []

        for i in script_seq_list:
            split_seq = script_seq_list[count_1][0].split()
            count_1 += 1
            print("Now looking for", split_seq)
            count_2 = 0

            for j in splitted_srt:
                if split_seq[0] == j:
                    count_2 += 1
                    if split_seq[1] == splitted_srt[count_2]:
                        count_2 += 1
                        if split_seq[2] == splitted_srt[count_2]:
                            count_2 += 1
                            if split_seq[3] == splitted_srt[count_2]:
                                count_2 += 1
                                if split_seq[4] == splitted_srt[count_2]:
                                    print("the sentence is at word number", count_2+2, "in the SRT")
                                    srt_sentence_index.append(count_2+2)
                                    break
                                else:
                                    count_2 -= 3
                                    continue
                            else:
                                count_2 -= 2
                                continue
                        else:
                            count_2 -= 1
                            continue
                    else:
                        continue
                else:
                    count_2 += 1
                    continue
    return srt_sentence_index


# This function receives a list containing the indexes of the critical words
# in the SRT file, then returns their corresponding TimeStamps
def find_ts_with_word_index(srt_sentence_index, path):
    ts_list = []
    with open(path, "r") as f:
        line = f.readline()
        word_count = 0
        tmp_ts = ''
        count = 0
        while line:
            if not line[0].isdigit():
                word_count += len((line.strip()).split())
                try:
                    if word_count >= int(srt_sentence_index[count]):
                        ts_list.append(tmp_ts)
                        count += 1
                except IndexError:
                    break
            if line[0] == '0':
                tmp_ts = line.replace('\n', '')
            line = f.readline()
        print(ts_list)
        return ts_list


# This function turns the script and SRT files into long strings that then
# are used for comparing them and doing further analysing
def creating_files_for_compare(srt_path, script_path, space_to_name):
    with open(srt_path, "r") as f:
        tmp_txt = open("tmp_srt.txt", "w")
        input = f.read()
        output = "".join(c for c in input if c not in punctuation)
        tmp_txt.write(output)

    with open('tmp_srt.txt', "r") as f:
        tmp_txt = open("comparison_srt.txt", "w")
        line = f.readline()
        while line:
            if not line[0].isdigit():
                line = line.replace("\n", " ")
                tmp_txt.write(line)
            line = f.readline()

    with open("comparison_srt.txt", "r") as f:
        tmp_txt = open("comparison_srt_1.txt", "w")
        line = f.readline()
        while line:
            line = re.sub("\s\s+", " ", line)
            tmp_txt.write(line)
            line = f.readline()

    with open(script_path, "r") as f:
        tmp_txt = open("tmp_script.txt", "w")
        input = f.read()
        output = "".join(c for c in input if c not in punctuation)
        tmp_txt.write(output)

    with open('tmp_script.txt', "r") as f:
        tmp_txt = open("comparison_script.txt", "w")
        line = f.readline()
        while line:
            ws_count = len(line) - len(line.lstrip(' '))
            if ws_count != space_to_name:
                line = line.strip(" ")
                line = line.replace("\n"," ")
                line = re.sub("\s\s+", " ", line)
                tmp_txt.write(line)
            line = f.readline()


# Checking the similarity between the SRT file and script file
def similarity_srt_script(str1, str2):
    with open(str1, "r") as s1:
        with open(str2, "r") as s2:
            str1 = s1.read()
            str2 = s2.read()
            print("Similarity between script and subtitle is", SequenceMatcher(None, str1, str2).ratio())











