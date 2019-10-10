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

def get_dev_line():
    section = "LINE"
    cp.read(cfpath)
    lin_ = cp[section]["line"]
    d = cp[section]["dev"]
    _line = None
    _dev = d
    ll =lin_.lower()
    idx = "linux".find(ll)
    print(idx, " idx")
    if ll == "win":
        _line="\r\n"
    elif ll == "lin":
        _line = "\n"
    elif ll == "mac":
        _line="\r"
    else:
        _line="\n"
    return _line, _dev
    pass

def write_path_line(path, line):
    """
    TODO: fix it
    :param path:
    :param line:
    :return:
    """
    l = "win"
    if line == "\r\n":
        l = "win"
    elif line == "\r":
        l = "mac"
    elif line == "\n":
        l = "lin"
    section = "LINE"
    cp[section]["line"] = l
    cp[section]["dev"] = path
    with open(cfpath, 'w') as cfg:
        cp.write(cfg)
    pass


def get_previous_values():
    """Still not used anywhere"""
    section="VALUES"
    cp.read(cfpath)
    startV, endV, points, array_size, idx, nplc = None, None, None, None, None, None
    try:
        startV = cp[section]['startv']
        endV = cp[section]['endv']
        points = cp[section]['points']
        array_size = cp[section]['array_size']
        idx = cp[section]['idx']
        nplc = cp[section]['nplc']
    except Exception as ex:
        print('ERR:CONF:00B')
        print(str(ex))
        pass
    return startV, endV, points, array_size, idx, nplc
    pass

def set_previous_values(dct):
    section="VALUES"
    try:
        cp[section]['startv']=str(dct['startV'])
        cp[section]['endv']=str(dct['endV'])
        cp[section]['points']=str(dct['points'])
        cp[section]['array_size']=str(dct['array_size'])
        cp[section]['idx']=str(dct['idx'])
        cp[section]['nplc']= str(dct['nplc'])
        with open(cfpath, 'w') as cfg:
            cp.write(cfg)
    except Exception as ex:
        print("ERR:CONF:00A")
        print(str(ex))
    pass

def getGPIOip():
    section = "RPGPIO"
    cp.read(cfpath)
    ip = None
    # try:
    ip = cp[section]['ip']
    print(ip, ' IP')
    # except Exception as ex:
    #     print(ex, ' ERR')
    #     pass
    return ip
