# @file    generatorAreaMap
# @author  Niel Jon Carl Aguel
# @date    2020-12-03

import os
import sys
import argparse
import overpy
import requests

CLI=argparse.ArgumentParser()
CLI.add_argument(
  "--area",  
  nargs="*",  
  type=int,
  default=[],  
)
CLI.add_argument(
  "--name",  
  type=str,
  default="Map",
)

args = CLI.parse_args()
print("name: %r" % args.name)
print("areas: %r" % args.area)

name = args.name+".osm"
useragent = 'Aguel'
headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '"Google Chrome 80"',
    'Accept': '*/*',
    'Sec-Fetch-Dest': 'empty',
    'User-Agent': useragent,
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://overpass-turbo.eu',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'cors',
    'Referer': 'https://overpass-turbo.eu/',
    'Accept-Language': '',
    'dnt': '1',
}

s = ""
for a in args.area:
    s +="<query into=\"_\" type=\"area\"> <id-query type=\"area\" ref=\""+ str(3600000000 + a) +"\"/> </query> "

query = """
    <osm-script output="xml" output-config="" timeout="10000">
    <union> """ + s + """
    </union>
    <union into="_">
        <query into="_" type="way">
        <has-kv k="highway" modv="" v=""/>
        <has-kv k="highway" modv="not" regv="path"/>
        <has-kv k="highway" modv="not" regv="steps"/>
        <has-kv k="highway" modv="not" regv="raceway"/>
        <has-kv k="highway" modv="not" regv="bridleway"/>
        <has-kv k="highway" modv="not" regv="proposed"/>
        <has-kv k="highway" modv="not" regv="construction"/>
        <has-kv k="highway" modv="not" regv="elevator"/>
        <has-kv k="highway" modv="not" regv="bus_guideway"/>
        <has-kv k="highway" modv="not" regv="footway"/>
        <has-kv k="highway" modv="not" regv="cycleway"/>
        <has-kv k="foot" modv="not" regv="no"/>
        <area-query/>
        </query>
    </union>
    <union into="_">
        <item from="_" into="_"/>
        <recurse from="_" into="_" type="down"/>
    </union>
    <print e="" from="_" geometry="skeleton" ids="yes" limit="" mode="meta" n="" order="id" s="" w=""/>
    </osm-script>
    """
data = {
  'data': query
}

response = requests.post('https://overpass-api.de/api/interpreter', headers=headers, data=data)
with open(name, 'w+') as f:
    f.write(response.text.encode('utf8').decode('ascii', 'ignore'))
api = overpy.Overpass()
results = api.parse_xml(response.text)
