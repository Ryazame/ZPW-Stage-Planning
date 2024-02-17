select DISTINCT
School,
case 
	when Studierichting_stage like '%zorg%' then 'Verzorging'
	when Studierichting_stage like '%pleg%' then 'Verpleging'
	when Studierichting_stage like '%logi%' then 'Logistiek'
	when Studierichting_stage like '%kamer%' then 'Kamerdienst'
	else 'Andere'
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
	,'4u + 8u blokstage (woensdag 4u)','7')
	,'8 uur op ma-di-don-vrij , 4 uur op woe','7')
	,'4 (gewone stage)/ 8 (blokstage)','7')
	,'8 u op ma-di-don-vrij en 4 uur op woe','7')
	,'8u op vrijdag , 4u op woensdag','5.67')
	,'op woendag 4uur , op vrijdag 8u','5.67')
	,'op woensdag 4uur op vrijdag 8u','5.67')
	,'ma-di-don-vrij 8 uur , op woe 4 uur','7')
	,'4 (gewone stage) + 8 (blokstage)','7')
	,'4u gewone stage +8u blokstage','7')
	,'minimaal 13u per week','7.36')
	,'4 u op woensdag - ma-di-don-vrij 8 uur','7')
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
	,'volledigewekzoalseglieewekneme','7')
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
	,'4u + 8u blokstage (woensdag 4u)','7')
	,'8 uur op ma-di-don-vrij , 4 uur op woe','7')
	,'4 (gewone stage)/ 8 (blokstage)','7')
	,'8 u op ma-di-don-vrij en 4 uur op woe','7')
	,'8u op vrijdag , 4u op woensdag','5.67')
	,'op woendag 4uur , op vrijdag 8u','5.67')
	,'op woensdag 4uur op vrijdag 8u','5.67')
	,'ma-di-don-vrij 8 uur , op woe 4 uur','7')
	,'4 (gewone stage) + 8 (blokstage)','7')
	,'4u gewone stage +8u blokstage','7')
	,'minimaal 13u per week','7.36')
	,'4 u op woensdag - ma-di-don-vrij 8 uur','7')
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
	,'volledigewekzoalseglieewekneme','7')
	)as berekende_uren
	,uren_per_dag
	,stage_uren as Ingegeven_StageUren,
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
and School like '%da%vinci%'
