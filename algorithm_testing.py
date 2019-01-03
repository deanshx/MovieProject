import algorithm
import movie_player

spc_to_name = 32
spc_to_sent = 22
script_name = "blade2.txt"
subs_name = "subshrek.txt"

algorithm.script_clean(script_name, spc_to_name, spc_to_sent)
algorithm.csv_two_clks("clean_script.txt", spc_to_name, spc_to_sent)
algorithm.extract_clks("mycsv.csv")
algorithm.normal_clks("clks.csv")
algorithm.graph_plot("n_clks.csv")
algorithm.clean_subtitles(subs_name)


