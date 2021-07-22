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
