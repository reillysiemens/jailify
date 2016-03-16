#***REMOVED*** | ***REMOVED***@wwu.edu | 04 March 2016
#
#    The purpose of this program is to determine the file type of a given
# directory or archive and then extract the archive. It will also pull
# out the team name from the title of the directory/archive.

import os
import sys
import tarfile
import zipfile
import os.path
import mimetypes

def main(argv):
    """Check for correct number args, determine file type, extract 
       file, extract data from file.

    Args:
        argv (str): first arg should be the file name.
    Returns:
        None
    """

    # Check for correct number of args and get team name.
    if (len(sys.argv) == 2):
        file_name = argv[1]
        team_name = check_title(file_name)
    else:
        print("Incorrect number of arguments")
        sys.exit()

    # Determine and return the file type.
    file_type = inspect_file(file_name)

    # Extract based on file type
    extract(file_type, file_name)




def check_title(filename):
    """Retrieves the password from the name of the file.

    Args:
        filename (str): name of the file including file extension
    Returns:
        teamname (str): name of the team, which is file name minus the file
                        extension
    """
    if os.path.isfile(filename) or os.path.isdir(filename):
        teamname = os.path.splitext(filename)[0]
        return teamname
    else:
        print("file not found")
        sys.exit()

def inspect_file(command_line_argument):
    """Determines which type of file is given.

    Args:
        command_line_argument (str): the name of the file given on the command
                                     line.
    Returns:
        file_type (str): aborts if file is not a directory, gzip, zip or xz compressed file.
                         otherwise returns a string representing one of the four types.
    """
    if os.path.isdir(command_line_argument):
        file_type = "dir"
    elif mimetypes.guess_type(command_line_argument)[1] == 'bzip2':
        file_type = "bz2"
    elif mimetypes.guess_type(command_line_argument)[1] == 'gzip':
        file_type = "gz"
    elif zipfile.is_zipfile(command_line_argument):
        file_type = "zip"
    elif mimetypes.guess_type(command_line_argument)[1] == "xz":
        file_type = "xz"
    else:
        print("Type is unacceptable")
        sys.exit()

    return file_type


def extract(filetype, filename):
    """Determines what type of extraction should be used on the file and calls
       the appropriate extract function. Then returns the directory to be worked
       with.

    Args:
        filetype (str): the type of file. 'dir', 'zip', 'xz', 'bzip2' or 'gzip'.
        filename (str): the name of the file as provided from the command line.
                        Includes file extension.
    Returns:
        filelist (list): a list containing extracted file objects from the directory.
    """

    if filetype == "bz2" or filetype == "gz" or filetype == "xz":
        extract_tar(filename, filetype)
    elif filetype == "zip":
        extract_zip(filename)
    elif filetype == "dir":
        print("Deal with directory")
    else:
        print("error with file type in extract()")
        sys.exit()



### Extraction Functions ###


def extract_tar(filenametar, comptype):
    """Opens, extracts, and closes tar file that has been compressed with one of gzip, xz, and bzip2.

    Args:
        filenametar (str): the name of the file as provided on the command 
                           line.
        comptype    (str): the compression type (bzip2, gzip or xz) to be passed in when decompressing.
    Returns:
        L (list): the members as a list of TarExFile objects.
    """
    try:
        with tarfile.open(filenametar, 'r:{}'.format(comptype)) as tar: 
            for f in tar:
                if os.path.basename(f.name) == "metadata.json":
                    data = tar.extractfile(f).read()
                    print(data)
                elif os.path.basename(f.name).endswith('.pub'):
                    print(".pub")
    except tarfile.TarError:
        print("Couldn't open tarfile")


def extract_zip(zipfilename):
    """Opens, extracts, and closes zip files.

    Args:
        zipfilename (str): the name of the file as provided on the command line.
    Returns:
        L (list): the members of the archive extracted as file objects.
   """
    try:
        L = []
        with zipfile.ZipFile(zipfilename) as myzip:
            for n in myzip.namelist():
                L.append(myzip.open(n))
    except zipfile.BadZipFile:
       print("Couldn't extract zip file")

if __name__ == '__main__':
    main(sys.argv)
