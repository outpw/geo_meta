import json
import pandas as pd
from nltk.tokenize import word_tokenize
import re
import numpy as np
import os

#double slashes required for windows
os.chdir('C:\\Users\\phwh9568\\geometaanalytics')

#open up and prepare the solr catalog
file = open('geoSolrCat.json', encoding='utf-8')
data = json.load(file)
docs = data['response']['docs']

#open and prepare the search terms csv
#lower case all search Terms into new column
#remove unusual characters such as '(', ')', & '*' from lower case terms. This messes up regex
#tokenize lower case search terms into new column
#for search categories, replace nan values with blank string
terms = pd.read_csv('SearchTerms.csv', dtype={'Search Terms':str})
terms['lowTerms'] = terms['Search Term'].str.lower()
terms['lowTerms'] = terms.lowTerms.str.replace('\(|\)', '')
terms['lowTerms'] = terms.lowTerms.str.replace('\*', '')
terms['tkTerms'] = terms['lowTerms'].apply(word_tokenize)
terms['Second Category'] = terms['Second Category'].replace(np.nan, '', regex=True)
terms['Third Category'] = terms['Third Category'].replace(np.nan, '', regex=True)

#spit out new csv for later review if necessary
terms.to_csv('SearchTerms_tokens.csv', encoding='utf-8')

#iterate over terms
itemList = []
for i, row in terms.iterrows():
    phrase = row['Search Term']

    #counters for each field match
    descCount = 0
    rightsCount = 0
    geomCount = 0
    provCount = 0
    formCount = 0
    pubCount = 0
    titleCount = 0
    subjCount = 0
    creatorCount = 0
    spatialCount = 0

    #iterate over tokenized version of terms
    for token in row['tkTerms']:

        #search for each token in each solr record
        for doc in docs:

            #use regex expression to find token or pluralized token in all lower cased fields. if present, count.
            if re.findall(rf'\b{token}\b|\b{token}+s\b',doc['dc_description_s'].lower()):
                descCount += 1

            if re.findall(rf'\b{token}\b|\b{token}+s\b',doc['dc_rights_s'].lower()):
                rightsCount += 1

            if re.findall(rf'\b{token}\b|\b{token}+s\b',doc['layer_geom_type_s'].lower()):
                geomCount += 1

            if re.findall(rf'\b{token}\b|\b{token}+s\b',doc['dct_provenance_s'].lower()):
                provCount += 1

            if re.findall(rf'\b{token}\b|\b{token}+s\b',doc['dc_format_s'].lower()):
                formCount += 1

            if re.findall(rf'\b{token}\b|\b{token}+s\b',doc['dc_publisher_s'].lower()):
                pubCount += 1

            if re.findall(rf'\b{token}\b|\b{token}+s\b',doc['dc_title_s'].lower()):
                titleCount += 1

            #subject, creator, and spatial fields are lists, so must iterate over them
            for subj in doc['dc_subject_sm']:
                subTokens = word_tokenize(subj)
                for subTok in subTokens:
                    if re.findall(rf'\b{token}\b|\b{token}+s\b',subTok.lower()):
                        subjCount += 1

            #creator is missing from some records, hence IF statement
            if 'dc_creator_sm' in doc:
                for creator in doc['dc_creator_sm']:
                    subTokens = word_tokenize(creator)
                    for subTok in subTokens:
                        if re.findall(rf'\b{token}\b|\b{token}+s\b',subTok.lower()):
                            creatorCount += 1

            for place in doc['dct_spatial_sm']:
                subTokens = word_tokenize(place)
                for subTok in subTokens:
                    if re.findall(rf'\b{token}\b|\b{token}+s\b',subTok.lower().replace('-',' ')): #remove dash from placenames
                        spatialCount += 1

    #add field counts to a dict for each search phrase. This will become an item in a list
    item = dict(searchTerms=phrase,
                dc_description_count=descCount,
                dc_rights_count=rightsCount,
                layer_geom_type_count=geomCount,
                dct_provenance_count=provCount,
                dc_format_count=formCount,
                dc_publisher_count=pubCount,
                dc_title_count=titleCount,
                dc_subject_count=subjCount,
                dc_creator_count=creatorCount,
                dct_spatial_count=spatialCount,
                searchCat1=row['Search Category'],
                searchCat2=row['Second Category'],
                searchCat3=row['Third Category'])

    #add each phrase dict to a list
    itemList.append(item)

output = dict(data=itemList)

#write the data dict to a json file
with open('geoMatches.json', 'w', encoding='utf-8') as f:
    json.dump(output, f,  indent=3)

#sum the field matches
#first create variables for each field count
desc = 0
rights = 0
geom = 0
prov = 0
form = 0
publisher = 0
title = 0
subject = 0
creator = 0
spatial = 0

#iterate over itemList dict and sum all individual search term matches
for item in itemList:
    desc = desc + item['dc_description_count']
    rights = rights + item['dc_rights_count']
    geom = geom + item['layer_geom_type_count']
    prov = prov + item['dct_provenance_count']
    form = form + item['dc_format_count']
    publisher = publisher + item['dc_publisher_count']
    title = title + item['dc_title_count']
    subject = subject + item['dc_subject_count']
    creator = creator + item['dc_creator_count']
    spatial = spatial + item['dct_spatial_count']

#print results
print('desc: ',desc)
print('rights: ',rights)
print('geom: ',geom)
print('prov: ',prov)
print('form: ', form)
print('publisher: ',publisher)
print('title: ',title)
print('subject: ',subject)
print('creator: ',creator)
print('spatial: ',spatial)
