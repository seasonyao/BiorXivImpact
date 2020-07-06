import pandas as pd
import os
import sys

    
input_file = "Path/to/input/pickle"
phrases_df = pd.read_pickle(input_file)
phrases = phrases_df.tolist()

#The input pickle is generated using the key phrase extraction method described earlier. An alternate input could be a custom list of phrases like below rather than the input pickle file.
phrases = ["TU tagging", "Translating Ribosome Affinity Purification", "Multiple Annealing and Looping-Based Amplification Cycles (MALBAC)", "Multiple Annealing and Looping-Based Amplification Cycles", "MALBAC", "Genomics", "Exome", "Mass cytometry (CyTOF)", "CyTOF", "Mass cytometry", "Single molecule array", "Proximity Extension Assay", "NGS", "Smart-seq", "MARS-seq", "CEL-seq", "Drop-seq", "Microwell-seq", "inDrop", "Methylomics", "BS-seq", "Methyl-seq", "5hmC", "TAB-seq", "hMeDIP", "oxBS-seq", "hMeDIP-seq", "Chip-seq", "DamID", "FAIRE-seq", "HIC", "ATAC-seq", "NOME-seq", "Assay for Transposase Accessible Chromatin", "Metaboanalyst", "metabolight", "pubchem", "crispr"]


out_csv = "Path/to/output/csvFile"
out_json_file = "Path/to/output/jsonFile"


for phrase in phrases:
    print("Searching for phrase " + phrase)
    phrase_search = '\"' + phrase.lower() + '\"'
    os.system("Rscript biorxiv-scraper.R -o "+ out_csv + phrase.replace(" ", "_") + ".csv" + " " + phrase_search)
    


#here, we calculate phrases' raw frequency, normlized frequency, gradient of frequency, and normlized gradient, and then we save them as a .json file.
phrases_dict = {}

for phrase in phrases:
    phrase_result = pd.read_csv(out_csv + phrase+".csv", delimiter=r"\t")

    cal_year = lambda x : int(x['submitted'].split('-')[0])
    phrase_result['submitted'] = phrase_result.apply(cal_year, axis=1)
    
    years = phrase_result['submitted'].value_counts().index.tolist()
    years.sort()
    
    phrase = phrase.replace('_', ' ')
    
    phrase_raw_freq_per_year = []
    phrase_norm_freq_per_year = []
    phrase_gradient_per_year = []
    phrase_second_gradient_per_year = []
    phrase_norm_slop_per_year = []
    phrase_second_norm_slop_per_year = []
    
    biorxiv_age = [2014, 2015, 2016, 2017, 2018, 2019]
    #we get all paper numbers every year for calculating the normlized data
    total_papers_num_per_year = [796, 1590, 4176, 10290, 19974, 30299]
    
    #raw freq
    for i in range(len(biorxiv_age)):
        phrase_raw_freq_per_year.append(
            phrase_result[phrase_result["submitted"]==biorxiv_age[i]].shape[0])
        
    #norm freq
    for i in range(len(biorxiv_age)):
        phrase_norm_freq_per_year.append(
            phrase_result[phrase_result["submitted"]==biorxiv_age[i]].shape[0]/total_papers_num_per_year[i])
        
    #gradient
    for i in range(1, len(biorxiv_age)):
        phrase_gradient_per_year.append(
            phrase_result[phrase_result["submitted"]==biorxiv_age[i]].shape[0] -
            phrase_result[phrase_result["submitted"]==biorxiv_age[i-1]].shape[0])
        
    #second gradient
    for i in range(1, len(phrase_gradient_per_year)):
        phrase_second_gradient_per_year.append(
            phrase_gradient_per_year[i] - phrase_gradient_per_year[i-1])
        
    #norm_slop
    for i in range(1, len(biorxiv_age)):
        if phrase_result[phrase_result["submitted"]==biorxiv_age[i-1]].shape[0]==0:
            phrase_norm_slop_per_year.append(0)
        else:
            phrase_norm_slop_per_year.append(
                (phrase_result[phrase_result["submitted"]==biorxiv_age[i]].shape[0] -
                phrase_result[phrase_result["submitted"]==biorxiv_age[i-1]].shape[0])/
                phrase_result[phrase_result["submitted"]==biorxiv_age[i-1]].shape[0]
            )

    #second norm_slop
    for i in range(1, len(phrase_norm_slop_per_year)):
        if phrase_norm_slop_per_year[i-1]==0:
            phrase_second_norm_slop_per_year.append(0)
        else:
            phrase_second_norm_slop_per_year.append(
                (phrase_norm_slop_per_year[i] - phrase_norm_slop_per_year[i-1])/phrase_norm_slop_per_year[i-1])
            
    
    phrases_dict[phrase] = [phrase_raw_freq_per_year, phrase_norm_freq_per_year, phrase_gradient_per_year,
                            phrase_second_gradient_per_year, phrase_norm_slop_per_year, phrase_second_norm_slop_per_year]
    
with open(out_json_file, 'w') as fp:
    json.dump(phrases_dict, fp)