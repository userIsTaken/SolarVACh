import configparser
import sys, os

cfpath="Config/paths.cfg"

cp = configparser.ConfigParser()

def get_ip():
    cp.read(cfpath)
    section="PATHS"
    ip = cp[section]["ip"]
    return ip
    pass

def get_path():
    cp.read(cfpath)
    section="PATHS"
    path=cp[section]["path"]
    return path

def write_ip(ip):
    section="PATHS"
    cp[section]["ip"] = ip
    with open(cfpath, 'w') as cfg:
        cp.write(cfg)

def write_path(path):
    section = "PATHS"
    cp[section]["path"] = path
    with open(cfpath, 'w') as cfg:
        cp.write(cfg)
