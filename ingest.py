import yaml # pyyaml

def parseYaml(file):
    with open(file) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        return data
