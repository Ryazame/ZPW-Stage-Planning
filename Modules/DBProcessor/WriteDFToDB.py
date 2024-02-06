from DBProcessor import DebugLogger as l
log=l.CreateLog()

def DFToDB(df,db,Schema,if_exists='replace'):
    df.to_sql(Schema, con=db, if_exists=if_exists)
    log.debug('|> Dataframe written to schema: {} on DB'.format(Schema))

def DBClose(db):
    try:
        db.close()
        log.debug('|--> DB Gesloten ')
    except:
        log.debug('|--> DB was al afgesloten')

def DBCommit(db):
    try:
        db.commit()
        log.debug('|--> Alle benodigde data in de DB opgeslagen')
    except:
        log.debug('|--> Could not commit to DB')

def DBCloseAndCommit(db):
    ############################################
    log.debug('|--> Commiting to and Closing the DB')
    DBCommit(db)
    DBClose(db)

