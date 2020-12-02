## This is the code repository for the paper titled "The Impact of Preprint Servers in the Formation of Novel Ideas" accepted at EMNLP2020

Link to paper: https://www.aclweb.org/anthology/2020.sdp-1.6/


Step 1: Download Pubmed Open-Access subset

```bash
wget ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/*.xml.tar.gz
```

Step 2: Untar file to `data` folder

```bash
tar -xzf comm_use.A-B.xml.tar.gz --directory data/
```

Step 3: To process the PubMed files into a CSV format run the following script:
Before doing so please set the necessary paths. This will create a csv file for each input xml file

```
python scripts/get_pubmed_data.py
```

Step 4: Download bioRxiv data using the following sript.
Before doing so please set the necessary paths. This will create a csv file containing biorXiv records

```
python scripts/get_biorxiv_data.py
```

Step 5: Process the bioRxiv data to generate key phrases from every document by running the script
Before doing so please set the necessary paths. This will create a pickle file containing key phrases for every document abstract. If you wish to include full text please modify the function accordingly to include necessary fields from the dataframe.

```
python scripts/pytextrank_get_key_phrases.py
```

Step 6: We further filter out key phrases using some filters. You can modify these filters for the required results in the notebook
```
notebooks/preprocessing_for_key_phrases.ipynb
```

Step 7: Look up occurrences and generate the time series data for each phrase in PMC and bioRxiv. This generates a json file for the list of phrases searched for.
Before doing so please set the necessary paths as  well as set the index for the phrases you would like to search for.  The following scripts were used to generate this data

```
scripts/pmc_occurrences.py
scripts/biorxiv_occurrences.py
```

Our results comparing the proposed Bayesian Model and the baseline can be found in the notebook

```
notebooks/bayesian_modeling_compare_pmc_biorxiv.ipynb
```

We performed a study of how PMC and biorXiv respond to virus outbreaks in the recet past. The results can be found in the notebook
```
notebooks/study_of_response_to_virus_phrase.ipynb
```

We performed a study to measure how bioRxiv content correlates with PMC and how it has changed over time. The results can be found in the notebook
```
notebooks/study_of_correlation_between_biorxiv_and_pmc.ipynb
```


