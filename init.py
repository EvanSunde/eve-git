import os, hashlib
import struct



#reads the content of file at the given path
def read_file(path):
    with open(path, 'rb') as f:
        return f.read()
    

#writes the given content to the given path
def write_files(path, content):    
    with open(path, 'wb') as f:
        f.write(content)



# to create a directory for our repostry and initilize .git directory.
def init(repo):
    os.mkdir(repo)
    os.mkdir(os.path.join(repo, '.git'))
    for name in ['objects', 'refs', 'refs/heads']:
        os.mkdir(os.path.join(repo, '.git', name))
    write_files(os.path.join(repo,'.git', 'HEAD'), b'ref:refs/heads/master')
    print(f'initilized empty repository: {repo}')
    

# making hash table to save file type and size in zlib compressed format at the directory .git/objects/ad/cd in SHA-1 format

#computes the hash and write to object if write is true. return SHA-1 object hash as hex string.
def hash_object(data, obj_type, write = True):
    header = '{} {}'.format(obj_type,len(data)).encode
    full_data = header + b'\x00' + data
    sha1 = hashlib.sha1(full_data).hexdigest()
    if write:
        path = os.path.join('.git','objects',sha1[:2], sha1[2:])
        if not os.path.exists(path):
            os.makedirs(os.path.dirname(path),exist_ok=True)
            write_files(path.zlib.compress(full_data))
    return sha1




# Defining function for Git Index which stores path name, modification time, SHA-1 hash,etc which will contain all the files in the trees instead of only stagged file



#this function read git index and return list of IndexEntry objects/
def read_index():
    try:
        data = read_file(os.path.join('.git', 'index')) 
    except FileNotFoundError:                                               # error handling which will return empty list when file is not found
        return[]
    digest = hashlib.sha1(data[:-20]).digest()                              # to calculate SHA-1 hash of all file but last 20 Bytes since they are checksum of rest of the file
    assert digest == data[-20:], 'invalid index checksum'                   
    signature, version, num_entries = struct.unpack('!4sLL',data[:12])      # 4byte signature 4byte version 4byte no. of extries
    assert signature == b'DIRC', \
       'invalied index signature{}'.format (signature)                       
    assert version ==2, 'unknown index version {}'.format(version) 
    entry_data = data[12:-20]                                               # extract main body of file excluding signature version (12 bytes) and checksum (last 20 bytes)


