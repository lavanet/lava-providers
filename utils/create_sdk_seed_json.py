import subprocess
import yaml
import json
result = subprocess.check_output(f"curl https://public-rpc-testnet2.lavanet.xyz:443/rest/lavanet/lava/pairing/providers/LAV1",shell=True)
jsonFinal = {"testnet": {}}
jsonLoad = json.loads(result)
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