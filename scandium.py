import os
import glob
import gzip

TEMP_DIR = "scandium_apps/"

def app_is_system(filename):
    with open(filename) as app_properties:
        for line in app_properties:
            if "app_is_system=1" == line.rstrip():
                return True
        return False

def unzip_applications(archives):
    for archive in archives:
        with gzip.open(archive, 'rb') as g:
            s = g.read()

        save_path = archive[:-3]

        with open(save_path, 'w') as f:
            f.write(s)

def install_applications():
    for app in glob.glob1(TEMP_DIR, "*.apk"):
        print("Installing " + app.split("-")[0])
        os.system("adb install " + app)
        os.system("rm -f " + app)

def main():
    app_names = [f.split("-")[0] for f in glob.glob1(".", "*.properties") if not app_is_system(f)]
    archives = [a for a in glob.glob1(".", "*.apk.gz") if a.split("-")[0] in app_names]
    os.system("mkdir -p " + TEMP_DIR)

    unzip_applications(archives)
    install_applications()

    #os.system("rm -rf " + TEMP_DIR)










if __name__ == "__main__":
    main()
