# nautilus-exif
Add EXIF to Nautilus' list view columns!
<img align="center" width="3150" height="1358" alt="image" src="https://github.com/user-attachments/assets/5ce71125-809d-4981-b1b1-5774a87793d8" />


## What it does
This script adds extra columns in Nautilus' list view from images' EXIF information. The following tags are supported:
* Originally Taken (`DateTimeOriginal`)
* Camera Make (`Make`)
* Camera Model (`Model`)
* Shutter Speed (`ExposureTime`)
* Aperture (`FNumber`)
* ISO (`ISOSpeedRatings`)
* Exposure Compensation (`ExposureBiasValue`)
* GPS Location (via [reverse geocoding](https://pypi.org/project/reverse-geocode/))
* GPS Altitude (`GPSAltitude`)
* Flash Status (`Flash`)
* Resolution (`PixelXDimension` & `PixelYDimension`)
* Resolution in megapixels (`PixelXDimension` & `PixelYDimension`)

## Install

#### 1. Nautilus Python Bindings
Ensure that `nautilus-python` is installed. This package provides the necessary Python bindings for Nautilus.

**Fedora**
```
sudo dnf install nautilus-python
```
**Debian**
```
sudo apt install nautilus-python
```
**NixOS**
```
environment.systemPackages = with pkgs; [
    ...
    nautilus-python
];
```
#### 2. Python Dependencies
Install the necessary Python libraries for this program to run:
* [`py3exiv2`](https://launchpad.net/py3exiv2), [PyPI](https://pypi.org/project/py3exiv2/)
* [`reverse_geocode`](https://github.com/richardpenman/reverse_geocode/), [PyPI](https://pypi.org/project/reverse-geocode/)

**Most Systems (pip)**
```
pip3 install py3exiv2 reverse-geocode
```

#### 3. Install
Copy the script to `~/.local/share/nautilus-python/extensions/`. You may have to create this folder yourself first

#### 4. Restart Nautilus
Kill Nautilus with `nautilus -q`, and re-open the app.

#### 5. Enable EXIF Columns
Go to List View in Nautilus, and at the drop down menu select `Visible Columns`. From here you can enable new columns from EXIF information

## About & Credits
This project is based on @Hekel1989's [nautilus-extra-columns](https://github.com/Hekel1989/nautilus-extra-columns). However as the original project ceases development and doesn't work anymore with the GTK4 Nautilus, this project is created to add more features while ensuring compatibility. Although I probably wouldn't be updating this project too often, constructive issue reports, features suggestions and pull requests are very welcome.

This project wouldn't be here without:
* [`nautilus-extra-columns`](https://github.com/Hekel1989/nautilus-extra-columns) - The original project
* [`py3exiv2`](https://launchpad.net/py3exiv2) - For enabling reading the EXIF tags
* [`reverse-geocode`](https://github.com/richardpenman/reverse_geocode/) - For enabling offline reverse geocoding
* Authors of GNOME Files (`nautilus`)
