
## libimgsmlr

Implement the feature extraction function of the `imgsmlr` extension, in languages such as: `c(so file)`, `Python`. Other languages should probably call dynamic libraries to adapt.

When using the `PostgreSQL` extension [imgsmlr](https://github.com/postgrespro/imgsmlr), I found that the feature extraction functions provided by `imgsmlr` are all PostgreSQL functions. This poses a problem, as the files need to be uploaded to and stored in the database during testing. This is generally not possible in service development, where text is usually stored separately in the file system, and only paths and `pattern`, `signature` are stored in the database. Therefore, it is necessary to implement the feature extraction functions used by the service development language.

## Depends

This library depends on the gd library. Please install it yourself first.

On Mac OSX: `brew install gd`

On Linux: `yum install -y gd-devel`

## Installation

```
pip install --global-option=build_ext libimgsmlr
```

### Errors


If the following error is encountered on Mac OSX.
```
fatal error: 'gd.h' file not found
#include "gd.h"
```
The solution is to set the environment variable first:
```
export CFLAGS="-I$(brew --prefix gd)/include"
export LFDLAGS="-L$(brew --prefix gd)/lib"
```

## Examples

```python
from libimgsmlr import img2pattern, pattern2signature, shuffle_pattern
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="libimgsmlr test")
    parser.add_argument('filename',help='image (jpeg/png/gif) file')

    args = parser.parse_args()
    print("filename: %s" % (args.filename))
    filename = args.filename
    content = open(filename, "rb").read()
    try:
        pattern = img2pattern(content)
        pattern2 = shuffle_pattern(pattern)
        print("pattern: %s" % (pattern2.as_array()))
        signature = pattern2signature(pattern)
        print("signature: %s" % (signature))
    except ValueError as err:
        print("ERROR: img2pattern(%s) failed! %s" % (filename, err))
```

## go test

```
# On mac
export CGO_CFLAGS="-I$(brew --prefix gd)/include"
export CGO_LDFLAGS="-L$(brew --prefix gd)/lib"
sh go_test.sh image-file.jpg
```

## LICENSE

[MIT](./LICENSE)
