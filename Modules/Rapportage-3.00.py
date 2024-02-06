from DBProcessor import DebugLogger as l
from YearProcessor import Prep2023
import pandas as pd
import xlsxwriter as xw
import sqlite3
from datetime import date



log=l.CreateLog()
Year,RootDrive,FormFileNaam,BackupPath,ProcessDelta=Prep2023.GetParamsFromConfig(2023)
DBFilePath = "{0}Database\\Dataset_{1}.sqlite".format(RootDrive,Year)
# Year = 2022
# RootDrive = "C:\\Users\\rianne.hartman\\Documents\\Stage\\"
# print('The python root is: '+RootDrive)
# FormFileNaam = str(Year)+" - Zorgpunt Waasland, Cluster West_Stageaanvraag formulier.xlsx"
# BackupPath="C:\\Users\\rianne.hartman\\OneDrive - Zorgpunt Waasland\\Backup\\"

log.info('________________________________________________________________________________________________')
log.info('|--- De gebruikte programma settings zijn:')
log.info('| * Database : '+DBFilePath)
log.info('| * Schooljaar : {0}'.format(str(int(Year))+' - '+str(int(Year)+1)))
log.info('|--- Start Programma')
log.info('________________________________________________________________________________________________')


log.debug('|> Connect to DB')
db = sqlite3.connect(DBFilePath)
log.info('Connected to database: "{0}"'.format(DBFilePath))
MaxID = 0

DBQuery="""
select DISTINCT
School,
case 
	when lower(Studierichting_stage) like '%zorg%' then 'Verzorging'
	when lower(Studierichting_stage) like '%pleg%' then 'Verpleging'
	when lower(Studierichting_stage) like '%logi%' then 'Logistiek'
    when lower(Studierichting_stage) like '%kamer%' then 'Kamerdienst'
	else lower(Studierichting_stage)
end as Studierichting_stage,
[1]+[2]+[3]+[4]+[5]+[6]+[7]+[8]+[9]+[10]+[11]+[12]+[13]+[14]+[15]+[16]+[17]+[18]+[19]+[20]+[21]+[22]+[23]+[24]+[25]+[26]+[27]+[28]+[29]+[30]+[31] as AantalDagen,
case when stage_uren like '%dagen' then (cast(replace(stage_uren,'dagen','') as int)*7.6)
     when stage_uren like '%verzorgende:%' then SUBSTR(stage_uren,INSTR(stage_uren,'verzorgende'),LENGTH(stage_uren)-INSTR(stage_uren,'verzorgende'))
     when stage_uren like '%jaar%' then substr(uren_per_dag,1,1)*([1]+[2]+[3]+[4]+[5]+[6]+[7]+[8]+[9]+[10]+[11]+[12]+[13]+[14]+[15]+[16]+[17]+[18]+[19]+[20]+[21]+[22]+[23]+[24]+[25]+[26]+[27]+[28]+[29]+[30]+[31])
     when stage_uren like '%week%' then 8*([1]+[2]+[3]+[4]+[5]+[6]+[7]+[8]+[9]+[10]+[11]+[12]+[13]+[14]+[15]+[16]+[17]+[18]+[19]+[20]+[21]+[22]+[23]+[24]+[25]+[26]+[27]+[28]+[29]+[30]+[31])
     --when stage_uren like '%,%' then SUBSTR(stage_uren,1,INSTR(stage_uren,',')-1)
     else stage_uren
end as stage_uren,
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
#Results['Stage_txt']=Results.stage_uren.str.replace(r'(\d+[\,|\.\d]*)','')
#Results.dropna()
Results.drop(Results.AantalDagen)

DBQuery="""
select DISTINCT
School,
case 
	when lower(Studierichting_stage) like '%zorg%' then 'Verzorging'
	when lower(Studierichting_stage) like '%pleg%' then 'Verpleging'
	when lower(Studierichting_stage) like '%logi%' then 'Logistiek'
    when lower(Studierichting_stage) like '%kamer%' then 'Kamerdienst'
	else lower(Studierichting_stage)
end as Studierichting_stage,
[1]+[2]+[3]+[4]+[5]+[6]+[7]+[8]+[9]+[10]+[11]+[12]+[13]+[14]+[15]+[16]+[17]+[18]+[19]+[20]+[21]+[22]+[23]+[24]+[25]+[26]+[27]+[28]+[29]+[30]+[31] as AantalDagen,
trim(
	replace(
	replace(
	replace(
	replace(
	replace(
	replace(
	replace(
	replace(
	replace(
	replace(
	replace(
	replace(
	replace(
	replace(
	replace(
	replace(
	replace(
	replace(
	replace(
		(uren_per_dag)
	,'4u gewone stage + 8u blokstage','5.67')
	,'4 (gewone stage)/ 8 (blokstage)','5.67')
	,'4 (gewone stage) + 8 (blokstage)','5.67')
	,'4u gewone stage +8u blokstage','5.67')
	,'minimaal 13u per week','7.36')
	,'u',' ')
	,' ','')
	,'Aftespreken','7.36')
	,'gemiddeld','')
	,',','.')
	,'h','')
	,'..','.')
	,'/dag','')
	,'dag','')
	,'per','')
	,'ongeveer','')
	,'r','')
	,'/','7.36')
	,'volledigewekzoalseglieewekneme','7.36')+'.0'
)*([1]+[2]+[3]+[4]+[5]+[6]+[7]+[8]+[9]+[10]+[11]+[12]+[13]+[14]+[15]+[16]+[17]+[18]+[19]+[20]+[21]+[22]+[23]+[24]+[25]+[26]+[27]+[28]+[29]+[30]+[31])
as stage_uren,
trim(
	replace(
	replace(
	replace(
	replace(
	replace(
	replace(
	replace(
	replace(
	replace(
	replace(
	replace(
	replace(
	replace(
	replace(
	replace(
	replace(
	replace(
	replace(
	replace(
		(uren_per_dag)
	,'4u gewone stage + 8u blokstage','5.67')
	,'4 (gewone stage)/ 8 (blokstage)','5.67')
	,'4 (gewone stage) + 8 (blokstage)','5.67')
	,'4u gewone stage +8u blokstage','5.67')
	,'minimaal 13u per week','7.36')
	,'u',' ')
	,' ','')
	,'Aftespreken','7.36')
	,'gemiddeld','')
	,',','.')
	,'h','')
	,'..','.')
	,'/dag','')
	,'dag','')
	,'per','')
	,'ongeveer','')
	,'r','')
	,'/','7.36')
	,'volledigewekzoalseglieewekneme','7.36')+'.0'
)as berekende_uren,uren_per_dag,stage_uren as Ingegeven_StageUren,
lower(trim([Naam student]))as Naam,
CAST(Jaar as int) Jaar,
CAST(Maand as int) as Maand,
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
Results['Stage_num']=Results.stage_uren#.str.extract(r'(\d+[\,|\.\d]*)')
#Results['Stage_txt']=Results.stage_uren.str.replace(r'(\d+[\,|\.\d]*)','')
#Results.dropna()
Results.drop(Results.AantalDagen)


# In[8]:


############################################
#Close & Commit the Connection
try:
    db.commit()
    print('|--> Alle benodigde data in de DB opgeslagen')
    db.close()
    print('|--> DB Gesloten ')
except:
    print('|--> DB was al afgesloten')


# In[10]:


Waarden = Results[['School','Studierichting_stage','Naam','Jaar','Kwartaal','Stage_num','WCZ']].dropna()
#Waarden['Stage_num'] = Waarden['Stage_num'].str.replace(',','.').astype(float)
SubSet = Waarden.groupby(['School', 'Studierichting_stage','Jaar','Kwartaal','WCZ']).agg({'Stage_num': ['sum'],'Naam':pd.Series.nunique}).rename(columns={"Stage_num": "Aantal Uren", "Naam": "Studenten"})


# In[11]:


SubSet.to_excel("C:\\Users\\rianne.hartman\\Documents\\Stage\\OutPut\\Stage_Rapport_output_{0}.xlsx".format(Year))

