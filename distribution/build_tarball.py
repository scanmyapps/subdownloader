#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import re
import shutil
import zipfile
import commands

exclude_dirs = [".svn",".bzr","firesubtitles", "Subdownloader","build","dist","distribution"]
exclude_files = ["pyc", "~", "tmp", "xml", "e4p", "e4q", "e4s", "e4t", "zip", "cfg", "lockfile", "log", "build_tarball.py", "notes.py", "srt", "setup.py2exe.py", "subdownloader.1"]

def copy_to_temp(temp_path="/tmp/subdownloader"):
    sys.stdout.write("Copying current path contents to '%s'..."% temp_path)
    sys.stdout.flush()
    #os.mkdir("subdownloader_cli")
    shutil.copytree("..", os.path.join("..", temp_path))
    sys.stdout.write(" done\n")
    sys.stdout.flush()
    
def clean_temp(temp_path="/tmp/subdownloader", exclude_dirs=exclude_dirs):
    sys.stdout.write("Cleaning '%s'..."% temp_path)
    sys.stdout.flush()
    for root, dirs, fileNames in os.walk(temp_path):
        # check for unwanted directories
        if os.path.split(root)[-1] in exclude_dirs:
            shutil.rmtree(root)
            continue
        # check for unwanted files
        for fileName in fileNames:
            for ext in exclude_files:
                if re.search("%s$"% ext, fileName):
                    os.remove(os.path.join(root, fileName))
    sys.stdout.write(" done\n")
    sys.stdout.flush()
    
def clean_temp_cli(temp_path="/tmp/subdownloader", exclude_dirs=exclude_dirs):
    exclude_dirs.append("gui") # append another unwanted directory
    clean_temp(exclude_dirs=exclude_dirs)

def convert_to_cli(dir="/tmp/subdownloader"):
    # just a thing to replace some lines on the code
    fileName = 'run.py'
    f = open(os.path.join(dir, fileName))
    text = f.read()
    f.close()
    final = open(os.path.join(dir, fileName), 'w')
    text = text.replace("import gui.main", "pass")
    text = text.replace("gui.main.main(options)", "log.warning('GUI mode unavailable')")
    final.write(text)
    final.close()

def remove_temp(temp_path="/tmp/subdownloader"):
    sys.stdout.write("Removing temporary directory '%s'..."% temp_path)
    sys.stdout.flush()
    shutil.rmtree(temp_path)
    sys.stdout.write(" done\n")
    sys.stdout.flush()
    
def toZip( zipFile, directory="/tmp/subdownloader", compress_lib=zipfile):
    sys.stdout.write("Compressing '%s' to '%s'..."% (directory, zipFile))
    sys.stdout.flush()
    z = compress_lib.ZipFile(zipFile, 'w', compression=zipfile.ZIP_DEFLATED)
    for root, dirs, fileNames in os.walk(directory):
        for fileName in fileNames:
            if fileName is not zipFile: #avoid self compress
                filePath = os.path.join(root, fileName)
                z.write( filePath, os.path.join(filePath.lstrip("/tmp/")) )
    z.close()
    sys.stdout.write(" done\n")
    sys.stdout.flush()
    return zipFile
    
def get_svn_revision():
    commands.getoutput("cd ..;bzr update")
    version = commands.getoutput('bzr version-info --custom --template="{revno}"')
    return version


if __name__ == "__main__":
    svn_revision = get_svn_revision()
    zipName = "subdownloader-revision_%s.zip"% svn_revision
    # create the tarball directory tree
    copy_to_temp()
    if len(sys.argv) > 1:
        if sys.argv[1] == "-cli":
            zipName = "subdownloader_CLI-revision_%s.zip"% svn_revision
            # delete gui and other unwanted stuff
            clean_temp_cli()
            # replace some source code
            convert_to_cli()
        elif sys.argv[1] == "-gui":
            pass
    else:
        clean_temp()
    # create the tarball and delete the source directory
    toZip(zipName)
    # delete temporary directory
    remove_temp()
