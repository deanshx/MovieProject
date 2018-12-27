import algorithm

spc_to_name = 29
spc_to_sent = 17
script_name = "8MM.txt"
subs_name = "subshrek.txt"

algorithm.script_clean(script_name, spc_to_name, spc_to_sent)         # We need to automate the process of receiving these
algorithm.csv_two_clks("clean_script.txt", spc_to_name, spc_to_sent)  # We need to automate the process of receiving these
algorithm.extract_clks("mycsv.csv")
algorithm.normal_clks("clks.csv")
algorithm.graph_plot("n_clks.csv")
#algorithm.clean_subtitles(subs_name)
