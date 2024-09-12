
# libimgsmlr

Implement the feature extraction function of the `imgsmlr` extension, in languages such as: `c(so file)`, `Python`. Other languages should probably call dynamic libraries to adapt.

When using the `PostgreSQL` extension [imgsmlr](https://github.com/postgrespro/imgsmlr), I found that the feature extraction functions provided by `imgsmlr` are all PostgreSQL functions. This poses a problem, as the files need to be uploaded to and stored in the database during testing. This is generally not possible in service development, where text is usually stored separately in the file system, and only paths and `pattern`, `signature` are stored in the database. Therefore, it is necessary to implement the feature extraction functions used by the service development language.

## Depends

This library depends on the gd library. Please install it yourself first.

On Mac OSX: `brew install gd`

On Linux: `yum install -y gd-devel`

## Installation

```shell
pip install --global-option=build_ext libimgsmlr
```

### Errors

If the following error is encountered on Mac OSX.

```text
fatal error: 'gd.h' file not found
#include "gd.h"
```

The solution is to set the environment variable first:

```shell
export CFLAGS="-I$(brew --prefix gd)/include"
export LDFLAGS="-L$(brew --prefix gd)/lib"
```

## Examples

```py
import argparse
from libimgsmlr import img2pattern, pattern2signature, shuffle_pattern, pattern_distance, signature_distance


def image_pattern_signature(content):
    pattern = img2pattern(content)
    signature = pattern2signature(pattern)
    pattern = shuffle_pattern(pattern)
    return pattern, signature

def process_single_image(filename):
    content = open(filename, "rb").read()
    try:
        pattern, signature = image_pattern_signature(content)
        print(f"pattern: {pattern.as_array()}")
        print(f"signature: {signature}")
    except ValueError as err:
        print(f"Error: img2pattern({filename}) failed! {err}")

def calculate_distance(filename1, filename2):
    try:
        content1 = open(filename1, "rb").read()
        content2 = open(filename2, "rb").read()
        pattern1, signature1 = image_pattern_signature(content1)
        pattern2, signature2 = image_pattern_signature(content2)
        pattern_dist = pattern_distance(pattern1, pattern2)
        print(f"Pattern distance: {pattern_dist}")

        sig_dist = signature_distance(signature1, signature2)
        print(f"Signature distance: {sig_dist}")
    except ValueError as err:
        print(f"Error: Failed to calculate distance! {err}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="libimgsmlr test")
    parser.add_argument('filenames', nargs='+', help='Image files (jpeg/png/gif)')
    args = parser.parse_args()
    if len(args.filenames) == 1:
        process_single_image(args.filenames[0])
    elif len(args.filenames) == 2:
        calculate_distance(args.filenames[0], args.filenames[1])
    else:
        print("Please provide 1 or 2 image filenames")

```

## go test

```shell
# On mac
export CGO_CFLAGS="-I$(brew --prefix gd)/include"
export CGO_LDFLAGS="-L$(brew --prefix gd)/lib"
sh go_test.sh image-file.jpg
```

## LICENSE

[MIT](./LICENSE)
