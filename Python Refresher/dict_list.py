import json

json_str = (

    '{"a":[1,2],"b":"x","c":[3],"d":[4,5,6],"e":"hello",'

    '"f":[7,8],"g":"world","h":[9,10,11],"i":"python",'

    '"j":[12,13],"k":"chatgpt","l":[14,15,16]}'

)

data = json.loads(json_str)

for key, value in data.items():

    if isinstance(value, list):

        print(key)