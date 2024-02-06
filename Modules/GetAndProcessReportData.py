from DBProcessor import DebugLogger as l
from YearProcessor import Prep2023
from DBProcessor import WriteDFToDB
from tqdm import tqdm
# In[1]:

log=l.CreateLog()
Year,RootDrive,FormFileNaam,BackupPath,ProcessDelta=Prep2023.GetParamsFromConfig(2023)
log.debug('The python root is: '+RootDrive)


# In[2]:


#get_ipython().run_line_magic('pip', 'install xlsxwriter pandas')


# In[3]:

import pandas as pd
import sqlite3
import datetime
from datetime import date
import os
import xlsxwriter as xw
import datetime
import errno
import os
from os.path import exists
Min_Year = 2021
Current_Year = datetime.date.today().year
print('Running in: {}'.format(Current_Year))
Develop=False

# In[6]:


def check_pres(sub, test_str):
    for ele in sub:
        if ele in test_str:
            return 0
    return 1

def Return_HourValues_From_String(line):
    in_filt = [x if x in "0123456789.,/\\" else " " for x in line]
    in_join = str.join('', in_filt)
    number = in_join.split()
    returnvalue=list(number)
    re=[ele for ele in returnvalue if check_pres(ele, '/')]
    i=0
    Value1=8
    Value2=0
    Value3=4
    while i < len(re):
        if i==0:
            try:
                Value1=float(re[i].replace(',','.'))
                Value2=Value1
            except:
                Value1=7.6
        else:
            try:
                Value2=float(re[i].replace(',','.'))
                log.debug('Found Value2: {0}'.format(Value2))
                if Value2 > Value1:
                    Value3=Value1
                    Value1=Value2
                    Value2=Value3
                    log.debug('Corrected Value1 to {0}'.format(Value1))
                    log.debug('Corrected Value2 to {0}'.format(Value2))
                if Value2 == 0:
                    Value2=Value1
            except:
                Value2=Value1
                log.debug('{0} is an illegal Value, skipping'.format(re[i]))
        i += 1
    log.debug("Weekdays: {0} hours".format(Value1))
    log.debug("Wednesdays: {0} hours".format(Value2))
    Value=(Value1*4+Value2)/5   
    return Value


# In[7]:


def GetDGFilepath(RootDrive,Year):
    DBFilePath = RootDrive+"Database\\Dataset_"+str(Year)+".sqlite"
    log.debug('________________________________________________________________________________________________')
    log.debug('|--- De gebruikte programma settings zijn:')
    log.debug('| * Database : '+DBFilePath)
    log.debug('| * Schooljaar : '+str(Year)+' - '+str(Year+1))
    log.debug('|--- Start Programma')
    log.debug('________________________________________________________________________________________________')
    return DBFilePath


# In[8]:


def ConnectToDB(DBFilePath):
    file_exists = exists(DBFilePath)
    if file_exists:
        db = sqlite3.connect(DBFilePath)
    else:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), DBFilePath)
    return db


# In[9]:


def GetResultsFromDB(db):
    DBQuery="""
select DISTINCT
School,
case 
    when lower(Studierichting_stage) like '%zorg%' then 'Verzorging'
    when lower(Studierichting_stage) like '%pleg%' then 'Verpleging'
    when lower(Studierichting_stage) like '%kamer%' then 'kamerdienst'
	else lower(Studierichting_stage)
end as Studierichting_stage,
[1]+[2]+[3]+[4]+[5]+[6]+[7]+[8]+[9]+[10]+[11]+[12]+[13]+[14]+[15]+[16]+[17]+[18]+[19]+[20]+[21]+[22]+[23]+[24]+[25]+[26]+[27]+[28]+[29]+[30]+[31] as AantalDagen,
stage_uren,
uren_per_dag,
case 
    when lower(uren_per_dag) like '%woe%' then 1
    else 0 
end as Contains_woe,
lower(trim([Naam student]))as Naam,
CAST(Jaar as int) Jaar,
CASE 
    WHEN CAST(Maand as int) between 1 and 3 then 1
    WHEN CAST(Maand as int) between 4 and 6 then 2
    WHEN CAST(Maand as int) between 7 and 9 then 3
    WHEN CAST(Maand as int) between 10 and 12 then 4
END as Kwartaal,WCZ
from V_StageSet
where status = 'OK'
"""
    Results = pd.read_sql_query(DBQuery,db)
    Results['Stage_num']=Results.stage_uren.str.extract(r'(\d+[\,|\.\d]*)')
    return Results


# In[10]:


def CalculateHoursWorked(pd_results):
    pd_results['uren_per_dag_berekende'] = pd_results['uren_per_dag'].apply(Return_HourValues_From_String)
    pd_results['berekende_uren'] = pd_results['uren_per_dag_berekende']*pd_results['AantalDagen']
    return pd_results


# In[11]:


def CalculateSubset(pd_results):
    Waarden = pd_results[['School','Studierichting_stage','Naam','Jaar','Kwartaal','berekende_uren','WCZ','AantalDagen']].dropna()
    SubSet = Waarden.groupby(['School', 'Studierichting_stage','Jaar','Kwartaal','WCZ']).agg({'Naam':pd.Series.nunique,'AantalDagen': ['sum'],'berekende_uren': ['sum']}).rename(columns={"berekende_uren": "Aantal Uren", "Naam": "Studenten"})
    return SubSet


# In[12]:


def WriteToExcel(RootDrive,Year,Subset):
    ExcelOut="{0}\\OutPut\\Stage_Rapport_output_{1}.xlsx".format(RootDrive,Year)
    try:
        Subset.to_excel(ExcelOut)
    except Exception as e:
            print(e)


# In[13]:


def CloseCommitDB(db):
    ############################################
    #Close & Commit the Connection
    try:
        db.commit()
        log.debug('|--> Alle benodigde data uit de DB opgehaald')
        db.close()
        log.debug('|--> DB Gesloten ')
    except:
        log.debug('|--> DB was al afgesloten')


# In[14]:


def ProcessYear(RootDrive,Year):
    log.debug('Processing Year: {0}'.format(Year))
    DBFilePath=GetDGFilepath(RootDrive,Year)
    try:
        db=ConnectToDB(DBFilePath)
        Results=GetResultsFromDB(db)  
        WriteDFToDB.DBCloseAndCommit(db)
        Results=CalculateHoursWorked(Results)
        SubSet=CalculateSubset(Results)
        WriteToExcel(RootDrive,Year,SubSet)
    except Exception as e:
        log.error(e)
        log.warning('Database for year: {0} not found in : {1}...'.format(Year, DBFilePath))


# In[15]:


for Year in tqdm(range(Min_Year, Current_Year+1, 1), colour="MAGENTA", desc="Loading rapport..."):
    ProcessYear(RootDrive,Year)

