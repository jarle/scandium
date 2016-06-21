import os
import glob
import gzip
import subprocess

WORKDIR = "temp/"

def app_is_system(filename):
    with open(filename) as app_properties:
        for line in app_properties:
            if "app_is_system=1" == line.rstrip():
                return True
        return False

def unzip_application(archive):
    print("Unzipping %s" %archive)
    with gzip.open(archive, 'rb') as g:
        try:
            s = g.read()
        except IOError:
            print IOError

    save_path = archive[:-3]

    with open(save_path, 'w') as f:
        f.write(s)

    os.system("rm -f %s" %archive)
    return save_path

def install_application(app):
    print("Installing " + app.split("-")[0])
    os.system("adb install " + app)
    os.system("rm -f " + app)
    print("")

def main():
    os.system("mkdir -p " + WORKDIR)
    os.chdir(WORKDIR)
    adb_prop_cp = '''adb shell ls "/mnt/sdcard/TitaniumBackup/*.properties" | tr -d '\r' | xargs -i -n1 adb pull {} .'''
    adb_ls = ("adb", "shell", "ls", "/mnt/sdcard/TitaniumBackup/")
    os.system(adb_prop_cp + "> /dev/null 2>&1")
    app_names = [f.split("-")[0] for f in glob.glob1(".", "*.properties") if not app_is_system(f)]
    print("Found %d applications" % len(app_names))
    p = subprocess.Popen(adb_ls, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    archives = [a for a in p.stdout.read().splitlines() if a.split("-")[0] in app_names and a.endswith(".apk.gz")]

    for archive in archives:
        os.system("adb pull /mnt/sdcard/TitaniumBackup/%s ." %archive)
        app = unzip_application(archive)
        install_application(app)

if __name__ == "__main__":
    main()
