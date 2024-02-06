import pandas as pd
from DBProcessor import DebugLogger as l
log=l.CreateLog()

def ReadInputFile(ExcellFile):
    df = pd.read_excel(ExcellFile, index_col=0)
    df.reset_index(level=0, inplace=True)
    df = df.fillna(0)
    try:
        df = df.drop(['Start time','Completion time','Email','Name'], axis=1)
    except:
        df = df.drop(['Begintijd','Tijd van voltooien','E-mail','Naam'], axis=1)
    log.debug('|> Excel file ingelezen')
    return df

def ReadCorrectieFile(CorrectieFile):
    cf = pd.read_excel(CorrectieFile, index_col=0)
    log.debug('|> Correctiefile ingelezen')
    return cf
