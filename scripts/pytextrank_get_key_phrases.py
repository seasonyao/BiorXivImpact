import pandas as pd
import spacy
import pytextrank
import numpy as np

file_name = "Path/to/CSVFile"
output_name = "Path/to/output/pickle"


df = pd.read_csv(file_name, header=0,index_col=0)
df = df.dropna()
#df = df.iloc[:10]

global nlp
nlp = spacy.load('en_core_web_sm')

tr = pytextrank.TextRank()
nlp.add_pipe(tr.PipelineComponent, name='textrank', last=True)

#text = 'Compatibility of systems of linear constraints over the set of natural numbers. Criteria of compatibility of a system of linear Diophantine equations, strict inequations, and nonstrict inequations are considered.'
def get_key_phrases(x):
    try:
        text = x['abstract']
        doc = nlp(text)
        document_key_phrases = []
        for p in doc._.phrases:
            document_key_phrases.append([p.rank, p.count, p.text.lower()])
        return document_key_phrases
    except:
        return []
        
df['key_phrases_for_abstract'] = df.apply(get_key_phrases, axis=1)

df=df.drop(['title', 'publication_date', 'abstract', 'body'], axis=1)

df.to_pickle(output_name)