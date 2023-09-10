#ifndef __X_IMGSMLR_H__
#define __X_IMGSMLR_H__

#ifdef __cplusplus
extern "C"{
#endif

#include "gd.h"
#include <stdio.h>
#define PATTERN_SIZE 64
#define SIGNATURE_SIZE 16

typedef struct
{
    float values[PATTERN_SIZE][PATTERN_SIZE];
} Pattern;

typedef float Signature[SIGNATURE_SIZE];
int shuffle_pattern(Pattern* patternDst, Pattern* patternSrc);
int pattern2signature(Pattern* pattern, Signature signature);
Pattern* jpeg2pattern(void* img, int size, Pattern* pattern);
Pattern* png2pattern(void* img, int size, Pattern* pattern);
Pattern* gif2pattern(void* img, int size, Pattern* pattern);
Pattern* webp2pattern(void* img, int size, Pattern* pattern);

#ifdef __cplusplus
}
#endif

#endif
