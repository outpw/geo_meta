import json
import os

os.chdir('C:\\Users\\phwh9568\\geometaanalytics')

file = open('geoMatches.json', encoding = 'utf-8')
geo = json.load(file)

#function for tallying up category matches to fields
def catmap(cat):

    descCount = 0
    rightsCount = 0
    geomCount = 0
    provCount = 0
    formatCount = 0
    publisherCount = 0
    titleCount = 0
    subjCount = 0
    creatorCount = 0
    spatialCount = 0
    noneCount = 0

    global catList
    catList = []
    global catMap
    for item in geo['data']:
        if item['searchCat1'] == cat or item['searchCat2'] == cat or item['searchCat3'] == cat:
            if item['dc_description_count'] > 0:
                descCount += 1
            if item['dc_rights_count'] > 0:
                rightsCount += 1
            if item['layer_geom_type_count'] > 0:
                geomCount += 1
            if item['dct_provenance_count'] > 0:
                provCount += 1
            if item['dc_format_count'] > 0:
                formatCount += 1
            if item['dc_publisher_count'] > 0:
                publisherCount += 1
            if item['dc_title_count'] > 0:
                titleCount += 1
            if item['dc_subject_count'] > 0:
                subjCount += 1
            if item['dc_creator_count'] > 0:
                creatorCount += 1
            if item['dct_spatial_count'] > 0:
                spatialCount += 1
            catList.append(item['searchTerms'])

            if item['dc_description_count'] == 0 and item['dc_rights_count'] == 0 and item['layer_geom_type_count'] == 0 and item['dct_provenance_count'] == 0 and item['dc_format_count'] == 0 and item['dc_publisher_count'] == 0 and item['dc_title_count'] == 0 and item['dc_subject_count'] == 0 and item['dc_creator_count'] == 0 and item['dct_spatial_count'] == 0:
                noneCount += 1

    catMap = dict(cat=cat,
                  totalQueries= len(catList),
                  no_matches_count = noneCount,
                  matches_count = len(catList) - noneCount,
                  dc_description_count=descCount,
                  dc_rights_count=rightsCount,
                  layer_geom_type_count=geomCount,
                  dct_provenance_count=provCount,
                  dc_format_count=formatCount,
                  dc_publisher_count=publisherCount,
                  dc_title_count=titleCount,
                  dc_subject_count=subjCount,
                  dc_creator_count=creatorCount,
                  dct_spatial_count=spatialCount)
    return catMap

#list of all search term categories
categories = ['datatype', 'format', 'locational', 'organization', 'person', 'placename', 'publication', 'topical','unknown']

#loop over category list, write function output dicts into list.
dataList = []
for cat in categories:
    catmap(cat)
    dataList.append(catMap)

output = dict(data=dataList)

with open('catMatches_unique.json', 'w', encoding='utf-8') as f:
    json.dump(output, f,  indent=3)
