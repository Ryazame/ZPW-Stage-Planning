import json
CorrectDict = {
    '-':'_',
    ' ':'_',
    '__':'_',
    '()':''
}
with open("Modules/JSON/CorrectDict.JSON", "w") as fp:
    json.dump(CorrectDict, fp, indent=4)