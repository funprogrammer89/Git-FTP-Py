# Git-FTP-Py
Script to update ftp files based on Git commits.

Dependencies:
Python's Pip package installer
&
GitPython ('sudo pip3 install GitPython')

Only tested working with Linux.

A Python script that uploads/removes changed files according to git commits. Add 'post-commit' file in your git repo at '.git/hooks' and update the path inside the 'post-commit' file to point to the GitFTP.py file. You do not want to place the GitFTP.py file inside your repo directory because it contains your FTP credentials. You do not want the GitFTP file being uploaded to your FTP. Make sure the 'post-commit' file is executable by using 'chmod +x post-commit'. Update the FTP credentials in gitFTP.py. 

Now execute git commits to have the files automatically updated in your remote FTP.

Works with spaces in file names!

Known issues:

Not a big deal, but if you remove all files from a folder on a remote FTP directory, the folder will remain. Working on a fix. 2-26-23
