## geo_meta

This repository houses scripts and data for a project mapping search phrases entered into a GeoBlacklight instance to that repository's GeoBlacklight metadata. The search phrases came from Google Analytics. The Python scripts map the phrases to the GeoBlacklight catalog metadata fields and count successful mappings in two stages. First, summing successful matches to all fields to all search phrases (geoMatch.py), then classing the phrases into query type categories and summing the data by query type (catMatch_unique.py & catMatch_cumulative.py). Unique matches are at the catalog (metadata corpus) level while cumulative matches are at the record level.

### Query Types:

| Type         | Description                                                                         | Example                                          |
|-Datatype-----|-a specific type of geospatial data--------------------------------------------------|-"Basemap, contours"------------------------------|
| Format       | a specific type of file format                                                      | "Geotiff, shapefile"                             |
| Locational   | a general type of place                                                             | "Campsites, buildings"                           |
| Placename    | a specific place                                                                    | "Continental Divide, Colorado Springs"           |
| Organization | a corporate entity usually related to the creation or dissemination of the resource | "Colorado DOT, Census Bureau"                    |
| Person       | a specific individual                                                               | John Doe                                         |
| Publication  | a specific issuance of a particular resource                                        | "Census tracts, Bureau of Land Management roads" |
| Topical      | a general area or subject of interest                                               | "Agriculture, aliens"                            |
| Unknown      | the nature of the query could not be determined with certainty                      | "2000, trib"                                     |

### Data
- Input data are available in data/input/
- Output data are available in data/output/
