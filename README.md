# 7-Zip SFX, However as invoker

## How does it work?

By embedding [no-admin.manifest](./no-admin.manifest) to 7-Zip SFX file, the self-extracting files will have following features:
- Run under the AsInvoker permission
- HighDPI support

## Requirements

The necessary requirements are:
- Windows SDK 10.X
- Python 3.11

What's more, in order to automate build, ensure following command-line tools in the Path:
- 7z: decompresses the downloaded package and saves it to `cache/sdk`
- curl: download the 7z sdk and save it to `cache/download`


## Build

```
python main.py
```

You may find builds in release.

# License

LZMA SDK is placed in the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or distribute the original LZMA SDK code, either in source code form or as a compiled binary, for any purpose, commercial or non-commercial, and by any means.

Sfx-asinvoker is placed in the public domain, too.
