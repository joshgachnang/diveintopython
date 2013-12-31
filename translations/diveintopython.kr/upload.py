import boto
import os
import sys

BUCKET_NAME = 'kr.diveintopython.net'
ignored_folders = ('save', 'www.diveintopython.org', 'diveintopythonbak', '.git')
ignored_files = ('scrape.py', 'upload.py', 'scrape.py~', 'upload.py~', '.gitignore')

conn = boto.connect_s3()
bucket = conn.get_bucket(BUCKET_NAME)
sys.stdout.write("Beginning upload to %s" % BUCKET_NAME)

def check_ignore(dir, file):
    for fol in ignored_folders:
        if fol in dir:
            return True
    for f in ignored_files:
        if f == file:
            return True
    return False

def upload_file(arg, dirname, names):
    #'/'.join(a['href'].split('/')[8:])
    if len(dirname.split('/')) == 5:
        dir = '/'.join(dirname.split('/')[5:])
    else:
        dir = '/'.join(dirname.split('/')[5:]) + '/'
    print "dir is: %s" % dir 
    
    #print "dirname is %s, dir is %s" % (dirname, dir)
    for file in names:
        
        #print "full path is %s" % (dir + file)
        if os.path.isdir(dir + file):
            continue
        if check_ignore(dir, file) == True:
            continue
        sys.stdout.write("uploading ")
        sys.stdout.write(dir + file)
        sys.stdout.write('\n')
        key = boto.s3.key.Key(bucket=bucket, name=(dir + file))
        key.set_contents_from_filename((dir + file), cb=status, num_cb=10, policy="public-read")
        
        
    #if dirname == "":
        #key = boto.s3.key.Key(bucket=bucket, name=(name))
        #key.set_contents_from_filename((name), cb=status, num_cb=10, policy="public-read")
    #else:
        #key = boto.s3.key.Key(bucket=bucket, name=(dirname + '/' + name))
        #key.set_contents_from_filename((dirname + '/' + name), cb=status, num_cb=10, policy="public-read")
    #sys.stdout.write('\n')

def upload(directory):
    os.path.walk(directory, upload_file, 'arg')
    
def status(complete, total):
    sys.stdout.write('.')
    sys.stdout.flush()

    
if __name__ == '__main__':
    upload('/home/josh/programming/diveintopython.kr')