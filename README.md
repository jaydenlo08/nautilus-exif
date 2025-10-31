# nautilus-exif
Add EXIF to Nautilus' list view columns!
<img align="center" width="3150" height="1358" alt="image" src="https://github.com/user-attachments/assets/5ce71125-809d-4981-b1b1-5774a87793d8" />


## 🎉 What it does
This script adds extra columns in Nautilus' list view from images' EXIF information. The following tags are supported:
<details><summary><strong>🏷️ Supported EXIF Tags</strong></summary>
<div>

* Originally Taken (`DateTimeOriginal`)
* Camera Make (`Make`)
* Camera Model (`Model`)
* Shutter Speed (`ExposureTime`)
* Aperture (`FNumber`)
* ISO (`ISOSpeedRatings`)
* Exposure Compensation (`ExposureBiasValue`)
* Focal Length (`FocalLength`)
* GPS Location (via [reverse geocoding](https://pypi.org/project/reverse-geocode/))
* GPS Altitude (`GPSAltitude`)
* Flash Status (`Flash`)
* Resolution (`PixelXDimension` & `PixelYDimension`)
* Resolution in megapixels (`PixelXDimension` & `PixelYDimension`)
</div></details>

## 🧰 Install

<details><summary><strong>🐧 Most Systems</strong></summary>
<div>

#### 1. Nautilus Python Bindings
Ensure that `nautilus-python` is installed. This package provides the necessary Python bindings for Nautilus.

**Fedora**
```bash
sudo dnf install nautilus-python
```
**Debian**
```bash
sudo apt install nautilus-python
```

#### 2. Python Dependencies
Install the necessary Python libraries for this program to run:
* [`py3exiv2`](https://launchpad.net/py3exiv2), [PyPI](https://pypi.org/project/py3exiv2/)
* [`reverse_geocode`](https://github.com/richardpenman/reverse_geocode/), [PyPI](https://pypi.org/project/reverse-geocode/)
* [`pillow`](https://github.com/python-pillow/Pillow), [PyPI](https://pypi.org/project/pillow/)

```bash
pip3 install py3exiv2 reverse-geocode pillow
```

#### 3. Install
Copy the script to `~/.local/share/nautilus-python/extensions/`. You may have to create this folder yourself first

#### 4. Restart Nautilus
Kill Nautilus with `nautilus -q`, and re-open the app.

#### 5. Enable EXIF Columns
Go to List View in Nautilus, and at the drop down menu select `Visible Columns`. From here you can enable new columns from EXIF information
</div></details>

<details><summary><strong>❄️ NixOS (Home Manager)</strong></summary>
<div>

#### 1. Get Required Files
Clone this repository locally to the same directory as your `home.nix` (in `/etc/nixos/`). For example,

```
├── configuration.nix
├── hardware-configuration.nix
├── home.nix
└── nautilus-exif # Create this directory
    ├── default.nix
    └── nautilus-exif.py
```

#### 2. Modify your `home.nix`

```nix
{ inputs, lib, config, pkgs,  ... }:
let
  # Import package
  nautilus-exif = import ./nautilus-exif { inherit pkgs; };
  ...
in {
  home.packages = (with pkgs; [
    # Add to packages
    nautilus-exif
    ...
  ]);
  # Use new version of `Nautilus` for desktop
  xdg.desktopEntries."org.gnome.Nautilus" = {
    name = "Files";
    comment = "Access and organize files";
    terminal = false;
    type = "Application";
    exec = "${nautilus-exif}/bin/nautilus --new-window %U";
    startupNotify = true;
    icon = "org.gnome.Nautilus";
    categories = ["GNOME" "GTK" "Utility" "Core" "FileManager"];
    mimeType = ["inode/directory" "application/x-7z-compressed" "application/x-7z-compressed-tar" "application/x-bzip" "application/x-bzip-compressed-tar" "application/x-compress" "application/x-compressed-tar" "application/x-cpio" "application/x-gzip" "application/x-lha" "application/x-lzip" "application/x-lzip-compressed-tar" "application/x-lzma" "application/x-lzma-compressed-tar" "application/x-tar" "application/x-tarz" "application/x-xar" "application/x-xz" "application/x-xz-compressed-tar" "application/zip" "application/gzip" "application/bzip2" "application/x-bzip2-compressed-tar" "application/vnd.rar" "application/zstd" "application/x-zstd-compressed-tar"];
    actions."new-window" = {
      name = "New Window";
      exec = "${nautilus-exif}/bin/nautilus --new-window";
    };
  };
}
```

#### 3. Restart Nautilus
Kill Nautilus with `nautilus -q`, and re-open the app. You may need to log out and log back in for the new launcher to take effect.

#### 4. Enable EXIF Columns
Go to List View in Nautilus, and at the drop down menu select `Visible Columns`. From here you can enable new columns from EXIF information

</div></details>

## 💳 About & Credits
This project is based on @Hekel1989's [nautilus-extra-columns](https://github.com/Hekel1989/nautilus-extra-columns). However as the original project ceases development and doesn't work anymore with the GTK4 Nautilus, this project is created to add more features while ensuring compatibility. Although I probably wouldn't be updating this project too often, constructive issue reports, features suggestions and pull requests are very welcome.

This project wouldn't be here without:
* [`nautilus-extra-columns`](https://github.com/Hekel1989/nautilus-extra-columns) - The original project
* [`py3exiv2`](https://launchpad.net/py3exiv2) - For enabling reading the EXIF tags
* [`reverse-geocode`](https://github.com/richardpenman/reverse_geocode/) - For enabling offline reverse geocoding
* Authors of GNOME Files (`nautilus`)
