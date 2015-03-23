#!/usr/bin/python

import os, sys, getopt
import string, random, hashlib

def gen_random_data(minsize, maxsize):
    size = random.randint(minsize, maxsize)
    data = ''.join([random.choice(string.ascii_letters +
        string.digits) for n in xrange(size)])

    sha1 = hashlib.sha1(data).hexdigest()

    return data, sha1

def gen_file(dirpath, minsize, maxsize):
    data, sha1 = gen_random_data(minsize, maxsize)

    dirpath = dirpath + '/' + sha1[:2]
    if not os.path.exists(dirpath):
        os.makedirs(dirpath, 0755)

    name = dirpath + '/' + sha1[2:]
    file = open(name, 'w')
    file.write(data)
    file.close()

def walk_dirs(dirpath):
    os.chdir(dirpath)
    cwd = os.getcwd()
    for subdir, dirs, files in os.walk('./'):
        for d in dirs:
            os.chdir(cwd + '/' + d)
            for sub, di, files in os.walk('./'):
                for f in files:
                    fd = open(f, 'r')
                    rd = fd.read()
                    fd.close()

    os.chdir(cwd)

def main(prog, argv):
    numfiles = 2000
    maxsize  = 2048
    dirpath  = os.getcwd() + "/data"

    try:
        opts, args = getopt.getopt(argv,"n:s:d", ["numfiles=", "maxsize=", "dir="])
    except getopt.GetoptError:
        print prog, ' -n <numfiles> -s <maxsize> -d <dir>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print prog, ' -n <numfiles> -s <maxsize> -d <dir>'
            sys.exit()
        elif opt in ("-n", "--numfiles"):
            numfiles = int(arg)
        elif opt in ("-s", "--maxsize"):
            maxsize = int(arg)
        elif opt in ("-d", "--dir"):
            dirpath = arg

    print 'Num files is: ', numfiles
    print 'Max size is: ', maxsize

    if not os.path.exists(dirpath):
        os.makedirs(dirpath, 0755)

    walk_dirs(dirpath)
    return
    gen_file(dirpath, 10, maxsize)

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
