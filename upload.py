import boto
import os
import sys
import hashlib

BUCKET_NAME = 'www.diveintopython.net'
ignored_folders = ('save', 'www.diveintopython.org', 'diveintopythonbak', '.git')
ignored_files = ('scrape.py', 'upload.py', 'scrape.py~', 'upload.py~', '.gitignore')

conn = boto.connect_s3()
bucket = conn.get_bucket(BUCKET_NAME)

def check_ignore(dir, file):
    for fol in ignored_folders:
        if fol in dir:
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
            break
        md5.update(data)
    return md5

def upload_file(arg, dirname, names):
    #'/'.join(a['href'].split('/')[8:])
    files_changed = False

    if len(dirname.split('/')) == 5:
        dir = '/'.join(dirname.split('/')[5:])
    else:
        dir = '/'.join(dirname.split('/')[5:]) + '/'


    for file in names:
        sys.stdout.write('.')
        sys.stdout.flush()
        #print "full path is %s" % (dir + file)
        if os.path.isdir(dir + file):
            continue
        if check_ignore(dir, file) == True:
            continue
        localmd5sum = md5(dir + file) 
        
        # Check if file is already in bucket
        key = bucket.get_key(dir + file)
        
        if key == None:
            key = boto.s3.key.Key(bucket=bucket, name=(dir + file))
        else:
            etag = key.etag.strip('"').strip("'")
            if etag == localmd5sum.hexdigest():
                # MD5 is the same, so don't upload. Move along, nothing to
                # see here.
                continue
        
        # Mention to the user that we're going to do some uploading
        sys.stdout.write("uploading ")
        sys.stdout.write(dir + file)
        sys.stdout.write('\n')
        
        key = boto.s3.key.Key(bucket=bucket, name=(dir + file))
        # For better performance: md5= something. Couldn't get it working quickly.
        key.set_contents_from_filename((dir + file), cb=status, num_cb=10, policy="public-read",)
        files_changed = True
    return files_changed
    #if dirname == "":
        #key = boto.s3.key.Key(bucket=bucket, name=(name))
        #key.set_contents_from_filename((name), cb=status, num_cb=10, policy="public-read")
    #else:
        #key = boto.s3.key.Key(bucket=bucket, name=(dirname + '/' + name))
        #key.set_contents_from_filename((dirname + '/' + name), cb=status, num_cb=10, policy="public-read")
    #sys.stdout.write('\n')

def upload(directory):
    sys.stdout.write("Beginning upload to %s" % BUCKET_NAME)
    sys.stdout.flush()
    files_changed = os.path.walk(directory, upload_file, 'arg')
    if files_changed == False:
        print "\nNo files needed to be uploaded."
    
def status(complete, total):
    sys.stdout.write('.')
    sys.stdout.flush()

    
if __name__ == '__main__':
    upload('/home/josh/programming/diveintopython')