#!/usr/bin/python
import gi
import math
import reverse_geocode
from fractions import Fraction
from gi.repository import Nautilus, GObject
from datetime import datetime
from pyexiv2 import ImageMetadata as from_exiv

gi.require_version('Nautilus', '4.0')


class NecExif(GObject.GObject,
              Nautilus.ColumnProvider,
              Nautilus.InfoProvider, ):

    script_name = 'nautilus-exif.py'

    mime_do = [
        'image/jpeg', 'image/png', 'image/pgf', 'image/gif', 'image/bmp',
        'image/webp', 'image/targa', 'image/tiff', 'image/x-ms-bmp',
        'image/jp2', 'application/postscript', 'application/rdf+xml',
        'image/x-photoshop', 'image/heic', 'image/heif', 'image/avif',

        'image/x-exv', 'image/x-canon-cr2', 'image/x-canon-crw',
        'image/x-minolta-mrw', 'image/x-nikon-nef', 'image/x-pentax-pef',
        'image/x-panasonic-rw2', 'image/x-samsung-srw', 'image/x-olympus-orf',
        'image/x-fuji-raf'
    ]

    columns_setup = [
        {
            'name':        "NautilusPython::exif_datetime_original_column",
            'attribute':   "exif_datetime_original",
            'label':       "Originally Taken",
            'description': "Original date taken (EXIF)",
        },
        {
            'name':        "NautilusPython::exif_camera_make_column",
            'attribute':   "exif_camera_make",
            'label':       "Camera Make",
            'description': "Camera make (EXIF)",
        },
        {
            'name':        "NautilusPython::exif_camera_model_column",
            'attribute':   "exif_camera_model",
            'label':       "Camera Model",
            'description': "Camera model (EXIF)",
        },
        { #NEW
            'name':        "NautilusPython::exif_exposure",
            'attribute':   "exif_exposure",
            'label':       "Shutter Speed",
            'description': "Shutter Speed (EXIF)",
        },
        {
            'name':        "NautilusPython::exif_aperture_column",
            'attribute':   "exif_aperture",
            'label':       "Aperture",
            'description': "Aperture (EXIF)",
        },
        {
            'name':        "NautilusPython::exif_iso_column",
            'attribute':   "exif_iso",
            'label':       "ISO",
            'description': "ISO (EXIF)",
        },
        {
            'name':        "NautilusPython::exif_exposure_compensation_column",
            'attribute':   "exif_exposure_compensation",
            'label':       "Exposure Comp.",
            'description': "Exposure compensation (EXIF)",
        },
        {
            'name':        "NautilusPython::exif_gps_location_column",
            'attribute':   "exif_gps_location",
            'label':       "Location",
            'description': "GPS Location (EXIF)",
        },
        {
            'name':        "NautilusPython::exif_gps_altitude_column",
            'attribute':   "exif_gps_altitude",
            'label':       "GPS Altitude",
            'description': "GPS Altitude (EXIF)",
        },
        {
            'name':        "NautilusPython::exif_flash_column",
            'attribute':   "exif_flash",
            'label':       "Flash",
            'description': "Whether flash is used (EXIF)",
        },
        {
            'name':        "NautilusPython::exif_resolution_column",
            'attribute':   "exif_resolution",
            'label':       "Resolution",
            'description': "Image resolution (EXIF)",
        },
        {
            'name':        "NautilusPython::exif_megapixel_column",
            'attribute':   "exif_megapixel",
            'label':       "Megapixels",
            'description': "Image megapixels (EXIF)",
        },
    ]

    def __init__(self):
        print("* Starting {}".format(self.script_name))

    def get_columns(self):
        return [
            Nautilus.Column(
                name=col['name'],
                attribute=col['attribute'],
                label=col['label'],
                description=col['description']
            )
            for col in self.columns_setup]

    def update_file_info_full(self, provider, handle, closure, file_info):
        # Initialize columns with empty strings
        for col in self.columns_setup:
            file_info.add_string_attribute(col['attribute'], '')

        # Only process local files with supported mime types
        if file_info.get_uri_scheme() != 'file' or file_info.get_mime_type() not in self.mime_do:
            return Nautilus.OperationResult.COMPLETE

        # Get the local file path
        filename = file_info.get_location().get_path()
        if not filename:
            return Nautilus.OperationResult.COMPLETE

        try:
            # Extract EXIF metadata directly (synchronous)
            MapPyExiv2(filename).to(
                lambda k, v: file_info.add_string_attribute(k, v)
            )
        except Exception as error:
            print(f"[{self.script_name}] Error reading EXIF for {filename}: {error}")

        # Tell Nautilus the metadata is ready
        file_info.invalidate_extension_info()

        return Nautilus.OperationResult.COMPLETE


class MapPyExiv2:
    def __init__(self, filename) -> None:
        metadata = from_exiv(filename)
        metadata.read()

        self.map(metadata)

    def to(self, fun) -> None:
        for (k, v) in self.__dict__.items():
            fun(k, v)

    def map(self, i) -> None:
        if v := i.get('Exif.Photo.DateTimeOriginal'):
            self.exif_datetime_original = v.value.strftime("%-d %b %Y")
        
        if v := i.get('Exif.Image.Make'):
            self.exif_camera_make = v.value
        
        if v := i.get('Exif.Image.Model'):
            self.exif_camera_model = v.value
        
        if v := i.get('Exif.Photo.ExposureTime'):
            if v.value >= (1/3):
                self.exif_exposure = f"{round(float(v.value))} s"
            else:
                self.exif_exposure = f"1/{round(float(1/v.value))} s"
            
        if v := i.get('Exif.Photo.FNumber'):
            self.exif_aperture = f"ƒ/{round(float(v.value)) if round(float(v.value),1).is_integer() else round(float(v.value),1)}"
            
        if v := i.get('Exif.Photo.ISOSpeedRatings'):
            self.exif_iso = v.raw_value
            
        
        if v := i.get('Exif.Photo.ExposureBiasValue'):
            tolerance = 1e-6
            try:
                n = abs(round(v.value*3)/3)
            except:
                self.exif_exposure_compensation = "0"
            else:
                if v.value < 0:
                    d = "-"
                else:
                    d = "+"
                
                if n < 1:
                    if abs(n - 1/3) < tolerance:
                        self.exif_exposure_compensation = f"{d}⅓"
                    elif abs(n - 2/3) < tolerance:
                        self.exif_exposure_compensation = f"{d}⅔"
                    else:
                        self.exif_exposure_compensation = "0"
                else:
                    w = math.floor(n)
                    if abs(n - w - 1/3) < tolerance:
                        self.exif_exposure_compensation = f"{d}{str(w)}⅓"
                    elif abs(n - w - 2/3) < tolerance:
                        self.exif_exposure_compensation = f"{d}{str(w)}⅔"
                    else:
                        self.exif_exposure_compensation = f"{d}{str(w)}"
        
        if (x := i.get('Exif.GPSInfo.GPSLatitude')) and (y := i.get('Exif.GPSInfo.GPSLongitude')):
                x_dd = float(x.value[0]+x.value[1]/60+x.value[2]/3600)
                y_dd = float(y.value[0]+y.value[1]/60+y.value[2]/3600)
                x_ref = i.get('Exif.GPSInfo.GPSLatitudeRef').value
                y_ref = i.get('Exif.GPSInfo.GPSLongitudeRef').value

                if x_ref == 'S':
                    x_dd = -x_dd
                if y_ref == 'W':
                    y_dd = -y_dd

                loc = reverse_geocode.get((x_dd,y_dd))
                self.exif_gps_location = f"{loc['city']}, {loc['country']}"
            
        if v := i.get('Exif.GPSInfo.GPSAltitude'):
            self.exif_gps_altitude = f"{round(v.value)} m"
            
        if v := i.get('Exif.Photo.Flash'):
            self.exif_flash = "Yes" if (v.value == 1) else "No"

        if (x := i.get('Exif.Photo.PixelXDimension')) and (y := i.get('Exif.Photo.PixelYDimension')):
            self.exif_resolution = f"{x.value}x{y.value}"
            self.exif_megapixel = f"{round(x.value*y.value/1000000)} MP"
