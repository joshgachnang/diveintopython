import boto
import os
import sys

BUCKET_NAME = 'www.diveintopython.net'
ignored_folders = ('save', 'www.diveintopython.org', 'diveintopythonbak')
ignored_files = ('scrape.py', 'upload.py', 'scrape.py~', 'upload.py~')

def upload(directory):
    conn = boto.connect_s3()
    bucket = conn.get_bucket(BUCKET_NAME)
    sys.stdout.write("Beginning upload to %s" % BUCKET_NAME)
    
    
    for item in os.listdir(directory):
        
        if os.path.isdir(item) and item[0] != '.' and item not in ignored_folders: # ignore hidden folders
            subdir = item
            for file in os.listdir(subdir):
                if not os.path.isdir(file):
                    sys.stdout.write(subdir + '/' + file)
                    key = boto.s3.key.Key(bucket=bucket, name=(subdir + '/' + file))
                    key.set_contents_from_filename((subdir + '/' + file), cb=status, num_cb=10, policy="public-read")
                    sys.stdout.write('\n')
                    
        else:
            if not os.path.isdir(item) and item not in ignored_files and item[0] != '.': # ignore hidden files
                sys.stdout.write(item)
                key = boto.s3.key.Key(bucket=bucket, name=(item))
                key.set_contents_from_filename(item, cb=status, num_cb=10, policy="public-read")
                sys.stdout.write('\n')
def status(complete, total):
    sys.stdout.write('.')
    sys.stdout.flush()
    
if __name__ == '__main__':
    upload('/home/josh/programming/diveintopython')