import os, hashlib

def read_file(path):
    #reads the content of file at the given path
    with open(path, 'rb') as f:
        return f.read()
    

def write_files(path, content):
    #writes the given content to the given path
    with open(path, 'wb') as f:
        f.write(content)


def init(repo):
    # to create a directory for our repostry and initilize .git directory.
    os.mkdir(repo)
    os.mkdir(os.path.join(repo, '.git'))
    for name in ['objects', 'refs', 'refs/heads']:
        os.mkdir(os.path.join(repo, '.git', name))
    write_files(os.path.join(repo,'.git', 'HEAD'), b'ref:refs/heads/master')
    print(f'initilized empty repository: {repo}')
    

# making hash table to save file type and size in zlib compressed format at the directory .git/objects/ad/cd in SHA-1 format
def hash_object(data, obj_type, write = True):
    #computes the hash and write to object if write is true. return SHA-1 object hash as hex string.
    header = '{} {}'.format(obj_type,len(data)).encode
    full_data = header + b'\x00' + data
    sha1 = hashlib.sha1(full_data).hexdigest()
    if write:
         