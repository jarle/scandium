# scandium
Titanium Backup automatic installation of applications (tested on Ubuntu 16.04). Were you trying to restore your 100+ applications using Titanium Backup and received a prompt for installing every single one? This script will install those non-system applications automatically with the basic version of Titanium Backup root. 

## Usage

Connect your phone to your computer(with debugging enabled) and run the program:

```
python scandium.py
```

The script will look for non-system applications in the Titanium Backup folder on your phone and install them using adb. The script will not import system nor app settings as Titanium Backup already gives a convenient way of restoring them. 

## Dependencies

* android-tools-adb

## Todo

* Make the script cross-platform
* Create an android version(?)
