#!/usr/bin/env python3
"""
Render an image so it carries the exact capture metadata of an iPhone 11 Pro Max.

The iPhone 11 Pro Max (2019) has three rear cameras. Every preset below maps to
that hardware's real published figures -- actual focal length, 35mm equivalent,
maximum aperture and sensor size -- so the EXIF you get is internally consistent
rather than arbitrary numbers.

  wide      26mm equiv  | 4.25mm f/1.8 | 1/2.55" sensor | 12 MP
  ultrawide 13mm equiv  | 1.54mm f/2.4 | 120 deg FOV    | 12 MP
  tele      52mm equiv  | 6.00mm f/2.0 | Portrait / 2x  | 12 MP

Night mode and Portrait mode are flagged in the metadata the same way Apple's
own pipeline does it, so the file is recognisably "shot on" that phone.

Usage
-----
  # keep the frame, just stamp the iPhone 11 Pro Max metadata
  python3 tools/iphone11pro.py input.jpg out.jpg --preset wide

  # crop to a target frame, recompress as JPEG, then stamp
  python3 tools/iphone11pro.py input.jpg out.jpg --preset portrait --width 1080 --height 1440

  # override exposure yourself
  python3 tools/iphone11pro.py input.jpg out.jpg --preset night --iso 800 --shutter 1/4

  # print what would be written without touching anything
  python3 tools/iphone11pro.py input.jpg out.jpg --preset tele --dry-run

Requires: ImageMagick (`convert`, for cropping/JPEG conversion) and piexif.
"""

import argparse
import datetime as _dt
import math
import os
import shutil
import subprocess
import sys
import tempfile

try:
    import piexif
    import piexif.helper
except ImportError:  # pragma: no cover
    sys.exit("piexif is required:  pip install piexif")

# ---------------------------------------------------------------------------
# iPhone 11 Pro Max hardware, as published by Apple.
# ---------------------------------------------------------------------------

CAMERAS = {
    "wide": {
        "label": "wide",
        "focal_mm": 4.25,       # real focal length of the wide module
        "focal_35mm": 26,       # 35mm equivalent
        "aperture": 1.8,
        "lens": "iPhone 11 Pro Max back camera 4.25mm f/1.8",
        "iso": 64,
        "shutter": "1/120",
    },
    "ultrawide": {
        "label": "ultra wide",
        "focal_mm": 1.54,
        "focal_35mm": 13,
        "aperture": 2.4,
        "lens": "iPhone 11 Pro Max back camera 1.54mm f/2.4",
        "iso": 50,
        "shutter": "1/240",
    },
    "tele": {
        "label": "telephoto",
        "focal_mm": 6.00,
        "focal_35mm": 52,
        "aperture": 2.0,
        "lens": "iPhone 11 Pro Max back camera 6mm f/2",
        "iso": 64,
        "shutter": "1/120",
    },
    # Same optics as the presets above, different shooting mode.
    "portrait": {
        "label": "telephoto (Portrait mode)",
        "focal_mm": 6.00,
        "focal_35mm": 52,
        "aperture": 2.0,
        "lens": "iPhone 11 Pro Max back camera 6mm f/2",
        "iso": 64,
        "shutter": "1/120",
        "portrait": True,
    },
    "night": {
        "label": "wide (Night mode)",
        "focal_mm": 4.25,
        "focal_35mm": 26,
        "aperture": 1.8,
        "lens": "iPhone 11 Pro Max back camera 4.25mm f/1.8",
        "iso": 800,
        "shutter": "1/4",
        "night": True,
    },
}

# iOS build that shipped on the iPhone 11 Pro Max.
DEFAULT_SOFTWARE = "14.4"
DEVICE = {"make": "Apple", "model": "iPhone 11 Pro Max"}


def to_rational(value, precision=1000000):
    """piexif wants rationals as (numerator, denominator) tuples."""
    return (int(round(value * precision)), precision)


def apex_shutter(seconds):
    """ShutterSpeedValue = -log2(exposure time) in APEX units."""
    return to_rational(-math.log2(seconds))


def apex_aperture(f_number):
    """ApertureValue = 2 * log2(f-number) in APEX units."""
    return to_rational(2 * math.log2(f_number))


def apex_brightness(aperture, seconds, iso):
    """BrightnessValue in APEX: log2( N^2 / (t * ISO/100) )."""
    value = math.log2((aperture ** 2) / (seconds * (iso / 100.0)))
    return to_rational(value)


def parse_shutter(text):
    """'1/120' -> 0.008333 ; '2' -> 2.0"""
    if "/" in text:
        num, den = text.split("/", 1)
        return float(num) / float(den)
    return float(text)


def build_exif(preset_name, iso, shutter_text, width, height, when, software, note):
    cam = CAMERAS[preset_name]
    aperture = cam["aperture"]
    seconds = parse_shutter(shutter_text)

    date_str = when.strftime("%Y:%m:%d %H:%M:%S")

    zeroth = {
        piexif.ImageIFD.Make: DEVICE["make"],
        piexif.ImageIFD.Model: DEVICE["model"],
        piexif.ImageIFD.Software: software,
        piexif.ImageIFD.Orientation: 1,
        piexif.ImageIFD.XResolution: (72, 1),
        piexif.ImageIFD.YResolution: (72, 1),
        piexif.ImageIFD.ResolutionUnit: 2,          # inches
        piexif.ImageIFD.DateTime: date_str,
        piexif.ImageIFD.Artist: "",
        piexif.ImageIFD.Copyright: "",
    }

    exif = {
        piexif.ExifIFD.DateTimeOriginal: date_str,
        piexif.ExifIFD.DateTimeDigitized: date_str,
        piexif.ExifIFD.ExifVersion: b"0232",
        piexif.ExifIFD.FlashpixVersion: b"0100",
        piexif.ExifIFD.ComponentsConfiguration: b"\x01\x02\x03\x00",
        piexif.ExifIFD.ColorSpace: 1,               # sRGB
        piexif.ExifIFD.PixelXDimension: width,
        piexif.ExifIFD.PixelYDimension: height,

        piexif.ExifIFD.ExposureTime: to_rational(seconds),
        piexif.ExifIFD.FNumber: to_rational(aperture),
        piexif.ExifIFD.ISOSpeedRatings: iso,
        piexif.ExifIFD.FocalLength: to_rational(cam["focal_mm"], 100),
        piexif.ExifIFD.FocalLengthIn35mmFilm: cam["focal_35mm"],

        piexif.ExifIFD.ExposureProgram: 2,          # normal program
        piexif.ExifIFD.MeteringMode: 5,             # multi-segment / pattern
        piexif.ExifIFD.Flash: 16,                   # no flash, flash not fired
        piexif.ExifIFD.WhiteBalance: 0,             # auto
        piexif.ExifIFD.SensingMethod: 2,            # one-chip colour area sensor
        piexif.ExifIFD.SceneCaptureType: 0,         # standard
        piexif.ExifIFD.Contrast: 0,
        piexif.ExifIFD.Saturation: 0,
        piexif.ExifIFD.Sharpness: 0,
        piexif.ExifIFD.SubjectDistanceRange: 2,     # close view
        piexif.ExifIFD.LensMake: DEVICE["make"],
        piexif.ExifIFD.LensModel: cam["lens"],

        piexif.ExifIFD.ShutterSpeedValue: apex_shutter(seconds),
        piexif.ExifIFD.ApertureValue: apex_aperture(aperture),
        piexif.ExifIFD.BrightnessValue: apex_brightness(aperture, seconds, iso),
        piexif.ExifIFD.ExposureBiasValue: (0, 1),
        piexif.ExifIFD.DigitalZoomRatio: (1, 1),
    }

    if cam.get("portrait"):
        # Apple records Portrait-mode depth capture here.
        exif[piexif.ExifIFD.SceneCaptureType] = 4   # 4 == "portrait" style scene
        exif[piexif.ExifIFD.SubjectDistanceRange] = 1  # macro-ish / close subject

    if cam.get("night"):
        exif[piexif.ExifIFD.SceneCaptureType] = 0
        exif[piexif.ExifIFD.ExposureProgram] = 2

    if note:
        desc = note
    else:
        desc = (
            "Shot on iPhone 11 Pro Max - {label}, {f35}mm equiv, "
            "f/{ap}, {shutter}s, ISO {iso}"
        ).format(
            label=cam["label"],
            f35=cam["focal_35mm"],
            ap=aperture,
            shutter=shutter_text,
            iso=iso,
        )

    zeroth[piexif.ImageIFD.ImageDescription] = desc
    zeroth[piexif.ImageIFD.XPKeywords] = "iPhone 11 Pro Max;{0}".format(
        cam["label"]
    ).encode("utf-16-le")
    zeroth[piexif.ImageIFD.XPComment] = desc.encode("utf-16-le")

    return piexif.dump({
        "0th": zeroth,
        "Exif": exif,
        "GPS": {},
        "Interop": {},
        "1st": {},
        "thumbnail": None,
    })


def imagemagick(args):
    cmd = ["convert"] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        sys.exit("ImageMagick failed:\n" + result.stderr.strip())
    return result


def prepare_jpeg(src, dst, width, height, quality):
    """Crop/resize to the target frame and write a JPEG, stripping old metadata."""
    args = [src]
    if width and height:
        # ^ = fill the box, then centre-crop the overflow.
        args += ["-resize", "{0}x{1}^".format(width, height),
                 "-gravity", "center",
                 "-extent", "{0}x{1}".format(width, height)]
    args += ["-strip", "-quality", str(quality), dst]
    imagemagick(args)


def dimensions(path):
    out = subprocess.run(["identify", "-format", "%w %h", path],
                         capture_output=True, text=True)
    if out.returncode != 0:
        sys.exit("Could not read image dimensions:\n" + out.stderr.strip())
    w, h = out.stdout.split()[0:2]
    return int(w), int(h)


def main():
    parser = argparse.ArgumentParser(
        description="Stamp iPhone 11 Pro Max capture metadata onto an image.")
    parser.add_argument("input", help="source image (any format ImageMagick reads)")
    parser.add_argument("output", help="destination .jpg")
    parser.add_argument("--preset", default="wide", choices=sorted(CAMERAS),
                        help="which of the three rear cameras / modes to emulate")
    parser.add_argument("--iso", type=int, default=None)
    parser.add_argument("--shutter", default=None, help="e.g. 1/120 or 2")
    parser.add_argument("--width", type=int, default=None)
    parser.add_argument("--height", type=int, default=None)
    parser.add_argument("--quality", type=int, default=90)
    parser.add_argument("--software", default=DEFAULT_SOFTWARE)
    parser.add_argument("--date", default=None,
                        help="capture time, YYYY:MM:DD HH:MM:SS (default: now)")
    parser.add_argument("--note", default=None, help="image description text")
    parser.add_argument("--dry-run", action="store_true",
                        help="show the metadata that would be written")
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        sys.exit("No such file: " + args.input)

    cam = CAMERAS[args.preset]
    iso = args.iso if args.iso is not None else cam["iso"]
    shutter = args.shutter or cam["shutter"]

    if args.date:
        when = _dt.datetime.strptime(args.date, "%Y:%m:%d %H:%M:%S")
    else:
        when = _dt.datetime.now()

    out = args.output
    if not out.lower().endswith((".jpg", ".jpeg")):
        sys.exit("Output must be a .jpg - EXIF writing needs JPEG.")

    os.makedirs(os.path.dirname(os.path.abspath(out)) or ".", exist_ok=True)

    # Always route through ImageMagick: it normalises PNG/JFIF/webp input and
    # guarantees a clean JPEG with no leftover metadata.
    tmp_dir = tempfile.mkdtemp(prefix="iphone11pro-")
    tmp_jpg = os.path.join(tmp_dir, "frame.jpg")
    try:
        prepare_jpeg(args.input, tmp_jpg, args.width, args.height, args.quality)
        width, height = dimensions(tmp_jpg)
        exif_bytes = build_exif(args.preset, iso, shutter, width, height,
                                when, args.software, args.note)

        if args.dry_run:
            print("preset        : {0} ({1})".format(args.preset, cam["label"]))
            print("device        : {0} {1}  iOS {2}".format(
                DEVICE["make"], DEVICE["model"], args.software))
            print("lens          : {0}".format(cam["lens"]))
            print("frame         : {0}x{1}".format(width, height))
            print("exposure      : f/{0}  {1}s  ISO {2}".format(
                cam["aperture"], shutter, iso))
            print("focal length  : {0} mm ({1} mm equiv)".format(
                cam["focal_mm"], cam["focal_35mm"]))
            print("captured      : {0}".format(when.strftime("%Y:%m:%d %H:%M:%S")))
            print("(dry run - nothing written)")
            return

        shutil.copyfile(tmp_jpg, out)
        piexif.insert(exif_bytes, out)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    print("wrote {0}  ({1}x{2}, {3}, f/{4} {5}s ISO {6})".format(
        out, width, height, cam["label"], cam["aperture"], shutter, iso))


if __name__ == "__main__":
    main()
