from DBProcessor import DebugLogger as l
log=l.CreateLog()

def MakeDfBackup(df,BackupFullPathFileName):
    BackupFile = BackupFullPathFileName
    df.to_excel(BackupFile)
    log.debug('|> File backup gemaakt...')