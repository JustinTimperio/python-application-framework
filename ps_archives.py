#! /usr/bin/env python3
#### Archive Commands - v2.0
import os, gzip, tarfile, shutil, hashlib

#######################
### Gzip and Tar Functions 
###################
def GZ_C(path, rm=False):
    with open(path, 'rb') as f:
        with gzip.open(path + '.gz', 'wb') as gz:
            shutil.copyfileobj(f, gz)
    if rm == True:
        os.remove(path)
    if rm == False:
        return

def GZ_D(path, rm=False):
    with gzip.open(path, 'rb') as gz:
        with open(path[:-3], 'wb') as f:
            shutil.copyfileobj(gz, f)
    if rm == True:
        os.remove(path)
    if rm == False:
        return

def Tar_Dir(path, rm=False):
    with tarfile.open(path + '.tar', 'w') as tar:
        for f in search_fs(path):
            tar.add(f, f[len(path):])
    if rm == True:
        shutil.rmtree(path)
    if rm == False:
        return

def Untar_Dir(path, rm=False):
    with tarfile.open(path, 'r:') as tar:
        tar.extractall(path[:-4])
    if rm == True:
        os.remove(path)
    if rm == False:
        return

def Checksum_File(file_path):
    if not os.path.exists(file_path):
        return str(file_path + ' : FILE MISSING!')
    size = os.path.getsize(file_path)
    if size == 0:
        return str(file_path + ' : 0')
    ### Checksum in python is slow as fuck so i'm ignoring anything larger than 1GB. 
    ### Hopefully I'll fix this later by using raw linux commands
    elif size > 1073741824:
        return str(file_path + ' : TOO LARGE!')
    ### Checksum file in chunks of ~250MB
    else: 
        with open(file_path, 'rb') as fh:
            m = hashlib.md5()
            while True:
                data = fh.read(268435456)
                if not data:
                    break
                m.update(data)
            return str(file_path + ' : ' + str(m.hexdigest()))

#######################
### Core gztar Commands
###################
def gztar_c(dir, queue_depth=round(os.cpu_count()*.75), rmbool=True):
    import multiprocessing, tqdm 
    files = search_fs(dir)
    with multiprocessing.Pool(queue_depth) as pool:
        r = list(tqdm.tqdm(pool.imap(gzip_compress_file, files),
                           total=len(files), desc='Compressing Files'))
    print('Adding Compressed Files to TAR....')
    tar_dir(dir)
    if rmbool == True:
        shutil.rmtree(dir)
    
def gztar_d(tar, queue_depth=round(os.cpu_count()*.75), rmbool=True):
    import multiprocessing, tqdm 
    print('Extracting Files From TAR....')
    untar_dir(tar)
    if rmbool == True:
        os.remove(tar)
    files = search_fs(tar[:-4])
    with multiprocessing.Pool(queue_depth) as pool:
        r = list(tqdm.tqdm(pool.imap(gzip_decompress_file, files),
                           total=len(files), desc='Decompressing Files'))
