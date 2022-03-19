import json
import os
import sqlite3

def _get_f2b_data(db_path):
    if not os.path.isfile(db_path):
        return []
    
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    results = cur.execute("""
        SELECT jails.name, 
        COUNT(bans.ip) AS bans,
        (SELECT DISTINCT bans.ip from bans where jails.name = bans.jail ORDER BY timeofban DESC) as last_ban,
        (SELECT DISTINCT bans.data from bans where jails.name = bans.jail ORDER BY timeofban DESC) as data
        FROM jails 
        LEFT JOIN bans ON jails.name=bans.jail 
        GROUP BY jails.name
        """).fetchall()
    con.close()
    return [{
        "name": name,
        "bans": bans,
        "last_ban": last_ban,
        "data": json.dumps(json.loads(data), indent=4, sort_keys=True) if data else None
    } for (name, bans, last_ban, data) in results]

swag_f2b = _get_f2b_data("/config/fail2ban/fail2ban.sqlite3")
host_f2b = _get_f2b_data("/dashboard/fail2ban/fail2ban.sqlite3")

output = json.dumps(swag_f2b + host_f2b, sort_keys=True)
print(output)
