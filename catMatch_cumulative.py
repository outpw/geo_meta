import json
import os

os.chdir('C:\\Users\\phwh9568\\geometaanalytics')

file = open('geoMatches.json', encoding = 'utf-8')
geo = json.load(file)

#function for tallying up category matches to fields
def catmap(cat):


    descTotal = 0
    rightsTotal = 0
    geomTotal = 0
    provTotal = 0
    formatTotal = 0
    publisherTotal = 0
    titleTotal = 0
    subjTotal = 0
    creatorTotal = 0
    spatialTotal = 0
    noneCount = 0
    global catList
    catList = []
    global catMap
    for item in geo['data']:
        if item['searchCat1'] == cat or item['searchCat2'] == cat or item['searchCat3'] == cat:
            if item['dc_description_count'] > 0:
                descTotal += item['dc_description_count']
            if item['dc_rights_count'] > 0:
                rightsTotal += item['dc_rights_count']
            if item['layer_geom_type_count'] > 0:
                geomTotal += item['layer_geom_type_count']
            if item['dct_provenance_count'] > 0:
                provTotal += item['dct_provenance_count']
            if item['dc_format_count'] > 0:
                formatTotal += item['dc_format_count']
            if item['dc_publisher_count'] > 0:
                publisherTotal += item['dc_publisher_count']
            if item['dc_title_count'] > 0:
                titleTotal += item['dc_title_count']
            if item['dc_subject_count'] > 0:
                subjTotal += item['dc_subject_count']
            if item['dc_creator_count'] > 0:
                creatorTotal += item['dc_creator_count']
            if item['dct_spatial_count'] > 0:
                spatialTotal += item['dct_spatial_count']
            catList.append(item['searchTerms'])

            if item['dc_description_count'] == 0 and item['dc_rights_count'] == 0 and item['layer_geom_type_count'] == 0 and item['dct_provenance_count'] == 0 and item['dc_format_count'] == 0 and item['dc_publisher_count'] == 0 and item['dc_title_count'] == 0 and item['dc_subject_count'] == 0 and item['dc_creator_count'] == 0 and item['dct_spatial_count'] == 0:
                noneCount += 1

    catMap = dict(cat=cat,
                  totalQueries= len(catList),
                  no_matches_count = noneCount,
                  matches_count = len(catList) - noneCount,
                  dc_description_total=descTotal,
                  dc_rights_total=rightsTotal,
                  layer_geom_type_total=geomTotal,
                  dct_provenance_total=provTotal,
                  dc_format_total=formatTotal,
                  dc_publisher_total=publisherTotal,
                  dc_title_total=titleTotal,
                  dc_subject_total=subjTotal,
                  dc_creator_total=creatorTotal,
                  dct_spatial_total=spatialTotal)
    return catMap

#list of all search term categories
categories = ['datatype', 'format', 'locational', 'organization', 'person', 'placename', 'publication', 'topical','unknown']

#loop over category list, write function output dicts into list.
dataList = []
for cat in categories:
    catmap(cat)
    dataList.append(catMap)

output = dict(data=dataList)

with open('catMatches_cumulative.json', 'w', encoding='utf-8') as f:
    json.dump(output, f,  indent=3)
