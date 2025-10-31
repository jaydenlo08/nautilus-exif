{ pkgs ? import <nixpkgs> {} }:

let
  # Create a Python environment with required libraries
  pythonEnv = pkgs.python3.withPackages (ps: with ps; [
    py3exiv2
    reverse-geocode
  ]);
in

pkgs.symlinkJoin {
  name = "nautilus-exif";
  paths = [ pkgs.nautilus ];  # Nautilus binary
  buildInputs = [ pkgs.makeWrapper ];

  # Add extension files and wrapped binary
  postBuild = ''
    # Create directories in $out
    mkdir -p $out/share/nautilus-python/extensions
    mkdir -p $out/bin

    # Copy the Python extension
    cp ${./nautilus-exif.py} $out/share/nautilus-python/extensions/

    # Wrap Nautilus binary
    wrapProgram $out/bin/nautilus \
      --set PYTHONPATH "${pythonEnv}/${pythonEnv.sitePackages}" \
      --prefix PATH : $PATH
  '';
}
