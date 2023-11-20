package libimgsmlr

/*
#cgo CFLAGS: -std=c11
#cgo LDFLAGS: -lgd -lm
#include "imgsmlr.h"
*/
import "C"
import (
	"database/sql/driver"
	"fmt"
	"net/http"
	"strings"
	"unsafe"
)

var (
	g_precision int = 8
)

// PatternSize represents the size of the pattern.
const PatternSize = C.PATTERN_SIZE

// SignatureSize represents the size of the signature.
const SignatureSize = C.SIGNATURE_SIZE

func SetSimFloatPrecision(precision int) {
	g_precision = precision
}

type SimFloat float32

func (f SimFloat) String() string {
	return fmt.Sprintf("%.*f", g_precision, f)
}

// Signature is a Go representation of the C Signature type.
type Signature [SignatureSize]SimFloat

func (sign Signature) String() string {
	builder := strings.Builder{}
	builder.WriteString("(")
	for idx := 0; idx < SignatureSize; idx++ {
		builder.WriteString(sign[idx].String())
		if idx < SignatureSize-1 {
			builder.WriteString(",")
		}
	}
	builder.WriteString(")")
	return builder.String()
}

func (sign Signature) Value() (driver.Value, error) {
	return sign.String(), nil
}

func (sign *Signature) Scan(input interface{}) error {
	str, ok := input.(string)
	if !ok {
		return fmt.Errorf("input is not a string")
	}

	str = strings.Trim(str, "()")
	parts := strings.Split(str, ",")
	if len(parts) != SignatureSize {
		return fmt.Errorf("invalid input format")
	}

	for i, part := range parts {
		part = strings.TrimSpace(part)
		value, err := fmt.Sscanf(part, "%f", &sign[i])
		if err != nil {
			return err
		}
		if value != 1 {
			return fmt.Errorf("failed to scan value at index %d", i)
		}
	}

	return nil
}

// Pattern is a Go representation of the C Pattern struct.
type Pattern [PatternSize][PatternSize]SimFloat

func (p Pattern) String() string {
	builder := strings.Builder{}
	builder.WriteString("(")

	for i := 0; i < PatternSize; i++ {
		builder.WriteString("(")
		for j := 0; j < PatternSize; j++ {
			builder.WriteString(p[i][j].String())
			if j < PatternSize-1 {
				builder.WriteString(", ")
			}
		}
		builder.WriteString(")")

		if i < PatternSize-1 {
			builder.WriteString(", ")
		}
	}

	builder.WriteString(")")

	return builder.String()
}

// Value 方法用于获取模式的值
func (p Pattern) Value() (driver.Value, error) {
	return p.String(), nil
}

// Scan 方法用于从字符串加载数据到 Pattern 结构
func (p *Pattern) Scan(input interface{}) error {
	str, ok := input.(string)
	if !ok {
		return fmt.Errorf("input is not a string")
	}

	str = strings.Trim(str, "()")
	parts := strings.Split(str, "), (")
	if len(parts) != PatternSize {
		return fmt.Errorf("invalid input format")
	}

	for i, part := range parts {
		values := strings.Split(part, ",")
		if len(values) != PatternSize {
			return fmt.Errorf("invalid input format")
		}

		for j, valStr := range values {
			_, err := fmt.Sscanf(valStr, "%f", &p[i][j])
			if err != nil {
				return err
			}
		}
	}

	return nil
}

// ShufflePattern shuffles the input pattern using the C function.
func ShufflePattern(pattern *Pattern) (patternNew *Pattern) {
	patternNew = new(Pattern)
	C.shuffle_pattern((*C.Pattern)(unsafe.Pointer(patternNew)), (*C.Pattern)(unsafe.Pointer(pattern)))
	return
}

// Pattern2Signature converts a pattern to a signature using the C function.
func Pattern2Signature(pattern *Pattern) (signature *Signature) {
	signature = new(Signature)
	C.pattern2signature((*C.Pattern)(unsafe.Pointer(pattern)), (*C.float)(unsafe.Pointer(signature)))
	return
}

// jpeg2Pattern converts a JPEG image to a pattern using the C function.
func jpeg2Pattern(img []byte, pattern *Pattern) *Pattern {
	return (*Pattern)(unsafe.Pointer(C.jpeg2pattern(unsafe.Pointer(&img[0]), C.int(len(img)), (*C.Pattern)(unsafe.Pointer(pattern)))))
}

// png2Pattern converts a PNG image to a pattern using the C function.
func png2Pattern(img []byte, pattern *Pattern) *Pattern {
	return (*Pattern)(unsafe.Pointer(C.png2pattern(unsafe.Pointer(&img[0]), C.int(len(img)), (*C.Pattern)(unsafe.Pointer(pattern)))))
}

// gif2Pattern converts a GIF image to a pattern using the C function.
func gif2Pattern(img []byte, pattern *Pattern) *Pattern {
	return (*Pattern)(unsafe.Pointer(C.gif2pattern(unsafe.Pointer(&img[0]), C.int(len(img)), (*C.Pattern)(unsafe.Pointer(pattern)))))
}

// webp2Pattern converts a WebP image to a pattern using the C function.
func webp2Pattern(img []byte, pattern *Pattern) *Pattern {
	return (*Pattern)(unsafe.Pointer(C.webp2pattern(unsafe.Pointer(&img[0]), C.int(len(img)), (*C.Pattern)(unsafe.Pointer(pattern)))))
}

func Img2Pattern(img []byte) (pattern *Pattern, err error) {
	pattern = new(Pattern)
	contentType := http.DetectContentType(img)
	switch contentType {
	case "image/jpeg":
		jpeg2Pattern(img, pattern)
	case "image/png":
		png2Pattern(img, pattern)
	case "image/gif":
		gif2Pattern(img, pattern)
	case "image/webp":
		webp2Pattern(img, pattern)
	default:
		err = fmt.Errorf("unsupported content-type: %s", contentType)
		pattern = nil
	}
	return
}
