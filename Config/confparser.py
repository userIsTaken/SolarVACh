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
