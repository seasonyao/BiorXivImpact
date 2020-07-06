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
python get_biorxiv_data.py
```

Step 5: Process the bioRxiv data to generate key phrases from every document by running the script
Before doing so please set the necessary paths. This will create a pickle file containing key phrases for every document abstract. If you wish to include full text please modify the function accordingly to include necessary fields from the dataframe.

```
python pytextrank_get_key_phrases.py
```

Step 6: Look up occurrences and generate the time series data for each phrase in PMC and bioRxiv. This generates a json file for the list of phrases searched for.
Before doing so please set the necessary paths as  well as set the index for the phrases you would like to search for. 


Step 7: Changepoint Detection

Step 8: Bayesian Modelling 

Step 9: Compare bioRxiv and PMC using Bayesian Modelling

Step 10: Study of viruses

Step 11: Correlation study


