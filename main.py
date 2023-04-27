import os.path
import subprocess
import urllib.request
from os.path import join
from pathlib import Path
from typing import Iterator
from shutil import copyfile


def create_folder():
    basedir = os.path.dirname(__file__)
    folders = [join(basedir, "build"),
               join(basedir, "cache"),
               join(basedir, f"cache{os.sep}download"),
               join(basedir, f"cache{os.sep}sdk")]
    for path in folders:
        os.mkdir(path) if not os.path.exists(path) else ...


def download_sdk():
    version_list = ["2201", "1900", "1604"]
    download_path = join(os.path.dirname(__file__), f"cache{os.sep}download")
    for version in version_list:
        filepath = join(download_path, f"{version}.7z")
        urllib.request.urlretrieve(f"https://www.7-zip.org/a/lzma{version}.7z", filepath)


def find_mt():
    output = subprocess.check_output(
        ["reg", "query", "HKLM\\SOFTWARE\\Microsoft\\Windows Kits\\Installed Roots", "/reg:32"])
    
    sdk_path = ""
    for line in output.decode().split("\r\n"):
        if line.strip().startswith("KitsRoot"):
            params = line.split("  ")
            sdk_path = Path(params[-1])
    
    assert sdk_path != ""
    mt_path = list(sdk_path.glob("bin/*/x86/mt.exe"))
    
    assert mt_path[0]
    return mt_path[0]


def embed_manifest(sfx_path: Path, mt_path: Path | None = None):
    mt = mt_path or find_mt()
    assert sfx_path.is_file()
    
    # https://learn.microsoft.com/en-us/windows/win32/sbscs/mt-exe
    subprocess.run(
        [mt, "-manifest", "no-admin.manifest", f"-outputresource:{sfx_path};#1"])


def embed_manifest_for_all():
    build_path = Path('./build')
    for sdk in Path("./cache/sdk").glob("lzma*"):
        if sdk.is_dir():
            sdk_build_path = build_path.joinpath(sdk.name)
            sdk_build_path.mkdir(exist_ok=True)
            for sfx in sdk.glob("bin/*.sfx"):
                copyfile(sfx, sdk_build_path.joinpath(sfx.name))
    for sfx in build_path.glob("lzma*/*.sfx"):
        print(f"Embed for {sfx}")
        embed_manifest(sfx)


def extract_7z(input: Path, output_dir: Path):
    subprocess.run(["7z", "x", input, f"-o{output_dir}"])


def extract_sdk(*version_list: Iterator[str]):
    cache_path = Path("./cache/sdk")
    cache_sdk = set(lzma7z.name for lzma7z in cache_path.glob(
        "lzma*") if lzma7z.is_dir())
    
    for version in version_list:
        sdk = f"lzma{version}"
        if sdk not in cache_sdk:
            extract_7z(
                Path(f"./cache/download/{sdk}.7z"), cache_path.joinpath(sdk))


if __name__ == "__main__":
    create_folder()
    download_sdk()
    extract_sdk(["2201", "1900", "1604"])
    embed_manifest_for_all()
