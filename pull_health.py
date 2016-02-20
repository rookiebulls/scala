# import scalalib
import requests
import json
import sqlite3
import base64


"""
CM_CONFIG = {"url": "http://ium-rel11.cloudapp.net:8080/CM", "username": "admin11", "password": "admin0okmnji9"}
URL = "%s/api/rest" % CM_CONFIG["url"]


def header():
    CM_LOGIN = {"username": CM_CONFIG["username"], "password": CM_CONFIG["password"]}
    login_info = {
                  "username" : "administrator", 
                  "password" : "12345678" 
                }
    r = requests.post("%s/auth/login" % URL, json=CM_LOGIN)
    # r = requests.post("%s/auth/login" % 'http://localhost:8080/CM/api/rest', json=login_info)
    authinfo = r.json()
    headers = {}
    for x in ("token", "apiToken", "apiLicenseToken"):
        headers[x] = authinfo[x]
    return headers

def list_players():
    # headers = header()
    r = requests.get("%s/players" % URL, params=dict(limit=0), headers=headers)
    res = r.json()
    # print res
    lists = res.get('list')
    players = [dict(id=list_['id'], name=list_['name']) for list_ in lists]
    # for list_ in lists:
        # players.append(dict(id=list_['id'], name=list_['name']))
    return players

def get_player_state(players):
    issued_players = []
    for player in players:
        r = requests.get("%s/players/%d/state" % (URL,player['id']), headers=headers)
        res = r.json()
        if res.get('state') != 'HEALTHY':
            player['state'] = res.get('state')
            player['lastReported'] = res.get('lastReported')
            issued_players.append(player)
        # print player
    return issued_players

def db_commit(players):
    try:
        conn = sqlite3.connect('data-dev.sqlite')
        cursor = conn.cursor()
        for player in players:
            cursor.execute('SELECT name FROM players WHERE name=?',(player['name'],))
            result = cursor.fetchall()
            print result
            # cursor.execute("INSERT INTO players (name) values (?)", ('1',))
            if result:
                print 'gotit'
                cursor.execute('UPDATE players SET last_player_issue=?, last_player_heartbeat=? \
                    WHERE name=?', (player['state'], player['lastReported'], player['name']))
                conn.commit()
            else:
                print 'nogotit'
                cursor.execute("INSERT INTO players (name, last_player_issue, last_player_heartbeat) \
                    values (?,?,?)", (player['name'], player['state'], player['lastReported']))
                conn.commit()
    except Exception, e:
        print e
        
    finally:
        cursor.close()
        conn.close()
"""

class PullHealth(object):
    """docstring for PullHealth"""
    def __init__(self, cm_id, url, username, password):
        self.cm_id = cm_id
        self.url = url
        self.username = username
        self.password = password


    @staticmethod
    def get_cm_address():
        try:
            conn = sqlite3.connect('data-dev.sqlite')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM contentmanagers')
            results = cursor.fetchall()
            return results
        except Exception, e:
            print e
        finally:
            cursor.close()
            conn.close()


    def header(self):
        CM_LOGIN = {"username": self.username, "password": base64.decodestring(self.password)}
        r = requests.post("%s/api/rest/auth/login" % self.url, json=CM_LOGIN)
        authinfo = r.json()
        headers = {x: authinfo[x] for x in ("token", "apiToken", "apiLicenseToken")}
        return headers


    def list_players(self):
        r = requests.get("%s/api/rest/players" % self.url, params=dict(limit=0), headers=self.header())
        res = r.json()
        lists = res.get('list')
        players = [dict(id=list_['id'], name=list_['name'], address=self.cm_id) for list_ in lists]
        return players


    def get_player_states(self):
        issued_players = []
        for player in self.list_players():
            r = requests.get("%s/api/rest/players/%d/state" % (self.url,player['id']), headers=self.header())
            res = r.json()
            if res.get('state') != 'HEALTHY':
                player['state'] = res.get('state')
                player['lastReported'] = res.get('lastReported')
                issued_players.append(player)
        return issued_players


    def run(self):
        try:
            conn = sqlite3.connect('data-dev.sqlite')
            cursor = conn.cursor()
            for player in self.get_player_states():
                cursor.execute('SELECT name FROM players WHERE name=? and cm_id=?',(player['name'], player['address']))
                result = cursor.fetchall()
                print result
                # cursor.execute("INSERT INTO players (name) values (?)", ('1',))
                if result:
                    print 'updating database'
                    cursor.execute('UPDATE players SET last_player_issue=?, last_player_heartbeat=? \
                        WHERE name=? and cm_id=?', (player['state'], player['lastReported'], player['name'], player['address']))
                    conn.commit()
                else:
                    print 'inserting queries'
                    cursor.execute("INSERT INTO players (name, last_player_issue, last_player_heartbeat, cm_id) \
                        values (?,?,?,?)", (player['name'], player['state'], player['lastReported'], player['address']))
                    conn.commit()
        except Exception, e:
            print e
            
        finally:
            cursor.close()
            conn.close

        



    

if __name__ == '__main__':
    cms = PullHealth.get_cm_address()
    for cm in cms:
        pull_health = PullHealth(*cm)
        print pull_health.run()
    