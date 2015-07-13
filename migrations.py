from sqlalchemy import Table

def rev1(meta, engine):
    deeds_table = Table('deeds', meta, autoload=True, autoload_with=engine)
    columns = [c.name for c in deeds_table.columns]
    #print(columns)
    if 'synced' not in columns:
        print("running migration")
        sql = "ALTER TABLE deeds ADD COLUMN synced INTEGER default 0;"
        print(sql)
        engine.execute(sql)
        return True
    
    return False

