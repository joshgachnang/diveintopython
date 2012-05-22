import boto
import os
import sys
import hashlib

BUCKET_NAME = 'www.diveintopython.net'
ignored_folders = ('save', 'www.diveintopython.org', 'diveintopythonbak', '.git')
ignored_files = ('scrape.py', 'upload.py', 'scrape.py~', 'upload.py~', '.gitignore')

conn = boto.connect_s3()
bucket = conn.get_bucket(BUCKET_NAME)
base_dir = '/home/josh/programming/diveintopython/new'

files_changed = False
def check_ignore(adir, file):
    if adir is not None:
        for fol in ignored_folders:
            if fol in adir:
                return True
    for f in ignored_files:
        if f == file:
            return True
    return False

# Handy tip from https://groups.google.com/forum/#!topic/boto-users/eg_Qae9Tz2U
def md5(fname):
    md5 = hashlib.md5()
    f = open(fname)
    while True:
        data = f.read(1024*1024)
        if not data:
            "Break"
            break
        md5.update(data)
    return md5

def upload_file(root, files):
    for filename in files:
        file_path = os.path.join(root, filename)
        file_rel_path = os.path.relpath(file_path, base_dir)
        print file_path, file_rel_path
       
        if len(file_rel_path.split('/')) > 1:
            dirname = file_rel_path.split('/')[-2]
        else:
            dirname = None

        if check_ignore(dirname, filename) == True:
            continue
        
        # Check if file is already in bucket
        key = bucket.get_key(filename)
  
        # Mention to the user that we're going to do some uploading
        sys.stdout.write("uploading ")
        sys.stdout.write(filename)
        sys.stdout.write('\n')
        
        key = boto.s3.key.Key(bucket=bucket, name=(file_rel_path))
        # For better performance: md5= something. Couldn't get it working quickly.
        key.set_contents_from_filename(file_path, cb=status, num_cb=10, policy="public-read",)
        files_changed = True

def upload(directory):
    sys.stdout.write("Beginning upload to %s\n" % BUCKET_NAME)
    sys.stdout.flush()
    
    for (root, dirs, files) in os.walk(base_dir):
        upload_file(root, files)
    
    if files_changed == False:
        print "\nNo files needed to be uploaded."
    
def status(complete, total):
    sys.stdout.write('.')
    sys.stdout.flush()

    
if __name__ == '__main__':
    upload('/home/josh/programming/diveintopython/new')