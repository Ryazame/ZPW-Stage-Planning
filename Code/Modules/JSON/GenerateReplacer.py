import json
ReplaceDict = {
    'bachelor':'',
    'brugopleiding':'',
    'Artevelde Hogeschool Gent':'Artevelde',
    'Hogeschool Gent':'HOGent',
    'HO_Gent':'HOGent',
    '(in het kader van TWE)':'',
    'gent':'Gent',
}
#json.dumps(ReplaceDict, indent = 4) 

with open("C:\\ZPW\\Stage\\Code\\Modules\\JSON\\ReplaceDict.JSON", "w") as fp:
    json.dump(ReplaceDict, fp, indent=4)