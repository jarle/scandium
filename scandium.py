import os
import glob
import gzip
import subprocess
import shutil

WORKDIR = "temp/"

def app_is_system(filename):
    with open(filename) as app_properties:
        for line in app_properties:
            if "app_is_system=1" == line.rstrip():
                return True
        return False

def unzip_application(archive):
    print("Unzipping %s" %archive)
    save_path = archive[:-3]
    s = open(save_path, 'wb')
    with gzip.open(archive, 'rb') as g:
        try:
        	shutil.copyfileobj(g, s)
        except IOError:
            print IOError

    os.remove(archive)
    return save_path

def install_application(app):
    print("Installing " + app.split("-")[0])
    os.system("adb install " + app)
    os.remove(app)
    print("")

def get_property_files():
    adb_prop_ls = ("adb", "shell", "ls", "/mnt/sdcard/TitaniumBackup/*.properties")
    p = subprocess.Popen(adb_prop_ls, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    property_files = [f for f in p.stdout.read().splitlines() if f.endswith(".properties")]
    for property_file in property_files:
	    os.system("adb pull %s" %property_file)

def main():
    try:
    	os.mkdir(WORKDIR)
    except OSError as e:
    	print e

    os.chdir(WORKDIR)
    get_property_files()
    app_names = [f.split("-")[0] for f in glob.glob1(".", "*.properties") if not app_is_system(f)]
    print("Found %d applications" % len(app_names))
    adb_ls = ("adb", "shell", "ls", "/mnt/sdcard/TitaniumBackup/")
    p = subprocess.Popen(adb_ls, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    archives = [a for a in p.stdout.read().splitlines() if a.split("-")[0] in app_names and a.endswith(".apk.gz")]

    for archive in archives:
        os.system("adb pull /mnt/sdcard/TitaniumBackup/%s ." %archive)
        app = unzip_application(archive)
        install_application(app)
        print archive

if __name__ == "__main__":
    main()
