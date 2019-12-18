#! /usr/bin/env python3
#### Linux Commands - v2.0
import os, sys, subprocess, re 

def prError(text): print("\u001b[31;1m{}\033[00m" .format(text))
def prSuccess(text): print("\u001b[32;1m{}\033[00m" .format(text))
def prWorking(text): print("\033[33m{}\033[00m" .format(text))
def prWarning(text): print("\033[93m{}\033[00m" .format(text))
def prChanged(text): print("\u001b[35m{}\033[00m" .format(text))
def prRemoved(text): print("\033[31m{}\033[00m" .format(text))
def prAdded(text): print("\033[94m{}\033[00m" .format(text))

######
### File System Commands and Short-Cuts
######
def Open_Permissions(path):
    os.system("sudo chmod -R 777 " + path)

def Search_FS(path, typ='list'):
    if typ.lower() in ['list', 'l']:
        return [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(path)) for f in fn]
    elif typ.lower() in ['set', 's']:
        return {os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(path)) for f in fn}
    else:
        sys.exit('Error: Type Must be List/Set!')

def RM_File(file_path, sudo):
    if sudo == True:
        if os.path.exists(file_path):
            os.system('sudo rm ' + file_path)
    elif sudo == False:
        if os.path.exists(file_path):
            os.system('rm ' + file_path)
    else:
        sys.exit('Error: Type Must be List/Set!')

def MK_Dir(dir, sudo):
    if sudo == True:
        if not os.path.exists(dir):
            os.system("sudo mkdir " + dir)
    elif sudo == False:
        if not os.path.exists(dir):
            os.system("mkdir " + dir)
    else:
        sys.exit('Error: Type Must be List/Set!')

def RM_Dir(dir_path, sudo):
    if sudo == True:
        if os.path.exists(dir_path):
            os.system('sudo rm -r ' + dir_path)
    elif sudo == False:
        if not os.path.exists(dir):
            os.system('rm -r ' + dir_path)
    else:
        sys.exit('Error: Type Must be List/Set!')

def Export_List(file_name, iterable):
    if os.path.exists(file_name):
        os.remove(file_name)
    with open(file_name, 'w') as f:
        for i in iterable:
            f.write("%s\n" % i)

def Read_List(file_name, typ='list'):
    if typ == 'list':
        l = list(open(file_name).read().splitlines())
    elif typ == 'set':
        l = set(open(file_name).read().splitlines())
    else:
        sys.exit('Error: Type Must be List/Set!')
    return l

def Size_Of_Files(file_list):
    ### Returns Size of Files in Bytes
    size = 0
    for f in file_list:
        try: size += os.path.getsize(f)
        except: pass
    return size

def Trim_Dir(file_list):
    trim = {p.split('/')[-1] for p in file_list}
    return trim

def Replace_Spaces(file_list):
    trim = {s.strip().replace(' ', '-') for s in file_list}
    return trim

######
### Terminal Commands
######
def Escape_Bash(astr):
    return re.sub("(!| |\$|#|&|\"|\'|\(|\)|\||<|>|`|\\\|;)", r"\\\1", astr)

def Distro_Name():
    ### Returns Distro Name From /etc/os-release
    os_name = subprocess.check_output('cat /etc/os-release | grep PRETTY_NAME= | cut -c 13-', shell=True)
    return str(os_name)[2:-3]

def Sed_Replace(pattern, file_path):
    os.system("sed -e'" + pattern + "' -i " + file_path)

def Uncomment_Line_Sed(pattern, file_path, sudo):
    if sudo == True:
        os.system("sudo sed -e'/" + pattern + "/s/^#//g' -i " + file_path)
    elif sudo == False:
        os.system("sed -e'/" + pattern + "/s/^#//g' -i " + file_path)

def Comment_Line_Sed(pattern, file_path, sudo):
    if sudo == True:
        os.system("sudo sed -e'/" + pattern + "/s/^#*/#/g' -i " + file_path)
    elif sudo == False:
        os.system("sed -e'/" + pattern + "/s/^#*/#/g' -i " + file_path)

######
### Linux System Package Commands
######
def pacman(package, arg='-S'):
    os.system("sudo pacman " + arg + " " + package)

def yum(package, arg='install'):
    os.system("sudo yum " + arg + " " + package)

def apt(package, arg='install'):
    os.system("sudo apt-get " + arg + " " + package)

def zypper(package, arg='install'):
    os.system("sudo zypper " + arg + " " + package)

def pip_install(packages, arg='install'):
    os.system("sudo pip " + arg + " " + packages)

def pacaur_install(packages, arg='-S'):
    os.system("pacaur " + arg +  packages)
