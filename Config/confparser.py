import configparser
import sys, os

cfpath="Config/paths.cfg"

cp = configparser.ConfigParser()

def get_path_ip():
    cp.read(cfpath)
    section="PATHS"
    path=cp[section]["path"]
    ip = cp[section]["ip"]
    return path, ip

def write_path_ip(path, ip):
    section = "PATHS"
    cp[section]["path"] = path
    cp[section]["ip"] = ip
    with open(cfpath, 'w') as cfg:
        cp.write(cfg)


def get_previous_values():
    """Still not used anywhere"""
    section="VALUES"
    cp.read(cfpath)
    startV, endV, points, array_size = None, None, None, None
    try:
        startV = cp[section]['startV']
        endV = cp[section]['endV']
        points = cp[section]['points']
        array_size = cp[section]['array_size']
    except Exception as ex:
        print(str(ex))
        pass
    return startV, endV, points, array_size
    pass

def set_previous_values(dct):
    section="VALUES"
    try:
        cp[section]['startV']=dct['startV']
        cp[section]['endV']=dct['endV']
        cp[section]['points']=dct['points']
        cp[section]['array_size']=dct['array_size']
        with open(cfpath, 'w') as cfg:
            cp.write(cfg)
    except Exception as ex:
        print("ERR:CONF:00A")
        print(str(ex))
    pass
