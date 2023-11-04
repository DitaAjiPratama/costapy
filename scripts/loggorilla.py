import datetime

def prcss(loc, msg):
    print(f"[loggorilla][{datetime.datetime.now()}][\033[32mprcss\033[39m][\033[95m{loc}\033[39m] {msg}")

def accss(loc, msg):
    print(f"[loggorilla][{datetime.datetime.now()}][\033[36maccss\033[39m][\033[95m{loc}\033[39m] {msg}")

def fyinf(loc, msg):
    print(f"[loggorilla][{datetime.datetime.now()}][\033[93mfyinf\033[39m][\033[95m{loc}\033[39m] {msg}")

def error(loc, msg):
    print(f"[loggorilla][{datetime.datetime.now()}][\033[31merror\033[39m][\033[95m{loc}\033[39m] {msg}")
