import algorithm
import movie_player

spc_to_name = 30
spc_to_sent = 20
script_name = "eli.txt"
subs_name = "elisub.txt"
normal_critical_speaker = 0.0
normal_critical_word = 0.0

algorithm.script_clean(script_name, spc_to_name, spc_to_sent)
algorithm.csv_two_clks("clean_script.txt", spc_to_name, spc_to_sent)
algorithm.extract_clks("mycsv.csv")
algorithm.normal_clks("clks.csv")

algorithm.graph_plot("n_clks.csv")

algorithm.extract_normal_word(normal_critical_speaker, "n_clks.csv")
algorithm.clean_subtitles(subs_name)
#normal_word = algorithm.finding_norm_critical_word("n_clks.csv")
critical_ts = algorithm.finding_ts(normal_critical_word, "clean_subtitles.txt")
algorithm.creating_files_for_compare("clean_subtitles.txt", "clean_script.txt", spc_to_name)
algorithm.similarity_srt_script("comparison_script.txt", "comparison_srt_1.txt")
#print(critical_ts)

