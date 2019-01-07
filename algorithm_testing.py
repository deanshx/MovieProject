import algorithm


spc_to_name = 37
spc_to_sent = 25
script_name = "shrek.txt"
subs_name = "subshrek.txt"
num_of_max = 3
num_of_min = 3


# Functions done on TXT files (srt and script) preparing for analysing
algorithm.script_clean(script_name, spc_to_name, spc_to_sent)
algorithm.csv_two_clks("clean_script.txt", spc_to_name, spc_to_sent)
algorithm.extract_clks("mycsv.csv")
algorithm.normal_clks("clks.csv")
algorithm.clean_subtitles(subs_name)
algorithm.creating_files_for_compare("clean_subtitles.txt", "clean_script.txt", spc_to_name)


# Functions done on CSV files or create a CSV file
algorithm.csv_two_clks("clean_script.txt", spc_to_name, spc_to_sent)
algorithm.extract_clks("mycsv.csv")
algorithm.normal_clks("clks.csv")


# Functions used to analyze the data
normal_critical_word_list = algorithm.derivative_and_find_index("n_clks.csv", num_of_max, num_of_min)

srt_sentence_index = algorithm.find_word_index_with_matching_sequences\
    (normal_critical_word_list, "comparison_script.txt", "comparison_srt_1.txt")

critical_ts = algorithm.find_ts_with_word_index(srt_sentence_index, "clean_subtitles.txt")
algorithm.similarity_srt_script("comparison_script.txt", "comparison_srt_1.txt")
algorithm.graph_plot("n_clks.csv")

