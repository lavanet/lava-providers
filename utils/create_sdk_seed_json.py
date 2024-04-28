import subprocess
import yaml
import json

success = False
jsonLoad = {}
for i in range(10): 
    try:
        result = subprocess.check_output(f"curl https://lav1.rest.lava.build:443/lavanet/lava/pairing/providers/LAV1",shell=True)
        jsonFinal = {"testnet": {}}
        jsonLoad = json.loads(result)
        if "stakeEntry" not in jsonLoad:
            print(f"Failed fetch attempt, {i} jsonLoad", jsonLoad)
            continue
        success = True
        break
    except: 
        print("Failed", i)

if not success:
    print("Failed sdk_seed_json")
    exit(-2)

for k in jsonLoad["stakeEntry"]:
    address = k['address']
    stake = int(k['stake']['amount'])
    for i in k['endpoints']:
        for x in i['api_interfaces']:
            if x == "tendermintrpc": 
                port = i['iPPORT']
                geolocation = str(i['geolocation'])
                print(geolocation, port)
                if geolocation not in jsonFinal['testnet']: 
                    jsonFinal['testnet'][geolocation] = []
                jsonFinal['testnet'][geolocation].append({
                "rpcAddress": port,
                "publicAddress": address,
                "stake": stake
                })
                break

def sortLambda(val):
    return val["stake"]

for i in jsonFinal["testnet"]:
    jsonFinal["testnet"][i].sort(key=sortLambda,reverse=True)
    for j in jsonFinal["testnet"][i]:
        del j["stake"]

with open('sdkSeedProviders.json', 'w+') as f:
    json.dump(jsonFinal, f, indent=4)