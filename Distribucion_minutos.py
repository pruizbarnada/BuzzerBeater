import requests
import xml.etree.ElementTree as ET
import pandas as pd
import openpyxl
import pytz

def login(user, password, matchid):
  base_url = "http://bbapi.buzzerbeater.com/"
  params_autent = {
        "login": user,
        "code": password
    }
  session = requests.Session()
  response = session.get(base_url, params=params_autent)
  boxscore = session.get(base_url + 'boxscore.aspx', params = {'matchid':matchid})
  xml_box = ET.fromstring(boxscore.content)

  return xml_box


def find_minutes(xml_root, matchid):
  with pd.ExcelWriter(f'minutes game {matchid}.xlsx', engine='openpyxl') as writer:

    for team in ['awayTeam', 'homeTeam']:

      df = pd.DataFrame(columns=["Jugador", "B", "E", "A", "AP", "P", "Titular"])
      team_code = xml_root.find(f"./match/{team}/teamName").text

      for child in xml_root.findall(f"./match/{team}/boxscore/player"):
        player = child.find("firstName").text + " " + child.find("lastName").text
        
        pg = child.find("minutes/PG").text
        sg = child.find("minutes/SG").text
        sf = child.find("minutes/SF").text
        pf = child.find("minutes/PF").text
        c = child.find("minutes/C").text

        starter = child.find("isStarter").text
        if starter == "True":
          starter = "X"
        else:
          starter = ""

        new_row = [player, int(pg), int(sg), int(sf), int(pf), int(c), starter]
        df.loc[len(df)] = new_row
      
    
      df.to_excel(writer, sheet_name=team_code, index=False)

  
  files.download(f'minutes game {matchid}.xlsx')


def minutes(user, password, matchid):
  xml_boxscore = login(user, password, matchid)
  find_minutes(xml_boxscore, matchid)


#Generate excel

##Uncomment and fill the following:
#user = 
#password = 
#matchid = 

minutes(user, password, matchid)
