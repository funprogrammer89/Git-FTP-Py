from git import Repo
import ftplib

ftp = ftplib.FTP("ftpupload.net")   # FTP URL
ftp.login("username", "password")  # FTP ([Username],[Password])
ftpPath = '/kennethpelliott.com/htdocs/test/'  # Make sure to end the full path with a /
ftp.cwd(ftpPath)    # FTP directory

repo = Repo('.')    # Git repo directory, '.' = same directory as this script
assert not repo.bare
git = repo.git
show = repo.git.show("--name-status", "--format=")

lines = show.splitlines()
M = list()    # Modified files list
A = list()    # Added files list
D = list()    # Deleted files list
R = list()    # Renamed files list
Temp = list()       # Temporary list needed for modification

for x in lines:
    if x[0:1] == 'M':
        M.append(x[2:])
    elif x[0:1] == 'A':
        A.append(x[2:])
    elif x[0:1] == "D":
        D.append(x[2:])
    elif x[0:1] == 'R':
        temp = x.split('\t')
        R.append(temp[1])
        R.append(temp[2])

if len(M) > 0:
    print('Modified files:\n')
    for x in M:
        print('- ' + x)
        try:
            ftp.delete(x)
            ftp.storbinary('STOR ' + x, open(x, 'rb'))
        except:
            print("Failed ftp modify of '" + x + "'")
else:
    print('\n~ No files have been modified ~')

if len(R) > 0:
    print('Renamed files:\n')
    count = 0
    while count < len(R):
        print("- Old file name : '" + R[count] + "' | New file name : '" + R[count + 1] + "'")
        try:
            ftp.delete(R[count])
            ftp.storbinary('STOR ' + R[count+1], open(R[count+1], 'rb'))
        except:
            print("Failed ftp file rename of '" + R[count] + "'")
        count = count + 2
else:
    print('\n~ No files have been renamed ~')

if len(A) > 0:
    print('\nAdding files:\n')
    for x in A:
        print('- ' + x)
        ftpSetPath = ftpPath
        ftp.cwd(ftpPath)
        Temp = x.split('/')
        try:
            count = 0
            createPath = ''
            while count < len(Temp)-1:
                createPath = createPath + Temp[count] + "/"
                try:
                    ftp.mkd(Temp[count])
                except:
                    pass
                ftpSetPath = ftpSetPath + Temp[count] + '/'
                ftp.cwd(ftpSetPath)
                count = count + 1
            ftp.storbinary('STOR ' + Temp[len(Temp) - 1], open(x, 'rb'))
        except:
            print("Failed ftp upload of  '" + x + "'")
else:
    print('\n~ No files to add ~\n')

if len(D) > 0:
    print('\nDeleting files:\n')
    for x in D:
        print('- ' + x)
        try:
            ftp.delete(x)
        except:
            print("Failed delete of '" + x + "'")
else:
    print('\n~ No files to delete ~\n')

ftp.quit()
