package main

import (
	"flag"
	"fmt"
	"os"

	imgsmlr "github.com/jie123108/libimgsmlr/libimgsmlr"
)

func main() {

	var filename string
	flag.StringVar(&filename, "filename", "", "test image filename")

	flag.Parse()
	if filename != "" {
		// 读取图像文件
		img, err := os.ReadFile(filename)
		if err != nil {
			fmt.Println("Error reading image file:", err)
			return
		}
		imgsmlr.SetSimFloatPrecision(6)
		pattern, err := imgsmlr.Img2Pattern(img)
		if err != nil {
			fmt.Println("Img2Pattern error:", err)
			return
		}
		pattern2 := imgsmlr.ShufflePattern(pattern)
		fmt.Printf("pattern: %+v\n", pattern2)
		signature := imgsmlr.Pattern2Signature(pattern)
		fmt.Printf("signature: %+v\n", signature.String())
	}
}
