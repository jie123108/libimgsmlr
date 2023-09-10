
#include "imgsmlr.h"
#include "gd.h"
#include <stdio.h>
#include <math.h>
#include <assert.h>
#include <string.h>

#define PATTERN_SIZE 64
#define SIGNATURE_SIZE 16

#define Min(a,b) (((a)<(b))?(a):(b))
#define Max(a,b) (((a)>(b))?(a):(b))


static void makePattern(gdImagePtr im, Pattern *pattern);
static void normalizePattern(Pattern *pattern);
static void waveletTransform(Pattern *dst, Pattern *src, int size);
static float calcSumm(Pattern *pattern, int x, int y, int sX, int sY);
static void shuffle(Pattern *dst, Pattern *src, int x, int y, int sX, int sY, int w);


/*
 * Extract signature from pattern.
 */
int pattern2signature(Pattern* pattern, Signature signature)
{
    int size = PATTERN_SIZE / 2;
	int i = 0;
	float mult = 1.0f;

	while (size > 1)
	{
		size /= 2;
		signature[i++] = mult * calcSumm(pattern, size, 0, size, size);
		signature[i++] = mult * calcSumm(pattern, 0, size, size, size);
		signature[i++] = mult * calcSumm(pattern, size, size, size, size);
		mult *= 2.0f;
	}
	signature[SIGNATURE_SIZE - 1] = pattern->values[0][0];

    return 0;
}

int shuffle_pattern(Pattern* patternDst, Pattern* patternSrc)
{
	int size = PATTERN_SIZE;
	memcpy(patternDst, patternSrc, sizeof(Pattern));
	while (size > 4)
	{
		size /= 2;
		shuffle(patternDst, patternSrc, size, 0, size, size, size / 4);
		shuffle(patternDst, patternSrc, 0, size, size, size, size / 4);
		shuffle(patternDst, patternSrc, size, size, size, size, size / 4);
	}

	return 0;
}

static void shuffle(Pattern *dst, Pattern *src, int x, int y, int sX, int sY, int w)
{
	int i, j;

	for (i = x; i < x + sX; i++)
	{
		for (j = y; j < y + sY; j++)
		{
			int ii, jj;
			int ii_min = Max(x, i - w),
				ii_max = Min(x + sX, i + w + 1),
				jj_min = Max(y, j - w),
				jj_max = Min(y + sY, j + w + 1);
			float sum = 0.0f, sum_r = 0.0f;

			for (ii = ii_min; ii < ii_max; ii++)
			{
				for (jj = jj_min; jj < jj_max; jj++)
				{
					float r = (i - ii) * (i - ii) + (j - jj) * (j - jj);
					r = 1.0f - sqrt(r) / (float)w;
					if (r <= 0.0f)
						continue;
					sum += src->values[ii][jj] * src->values[ii][jj] * r;
					sum_r += r;
				}
			}
			assert (sum >= 0.0f);
			assert (sum_r > 0.0f);
			dst->values[i][j] = sqrt(sum / sum_r);
		}
	}
}


/*
 * Make pattern from gd image.
 */
static void makePattern(gdImagePtr im, Pattern* pattern)
{
	int i, j;
	for (i = 0; i < PATTERN_SIZE; i++)
		for (j = 0; j < PATTERN_SIZE; j++)
		{
			int pixel = gdImageGetTrueColorPixel(im, i, j);
			float red = (float) gdTrueColorGetRed(pixel) / 255.0,
				  green = (float) gdTrueColorGetGreen(pixel) / 255.0,
				  blue = (float) gdTrueColorGetBlue(pixel) / 255.0;
			pattern->values[i][j] = sqrt((red * red + green * green + blue * blue) / 3.0f);
		}
}

/*
 * Normalize pattern: make it minimal value equal to 0 and
 * maximum value equal to 1.
 */
static void normalizePattern(Pattern* pattern)
{
	float min = 1.0f, max = 0.0f, val;
	int i, j;
	for (i = 0; i < PATTERN_SIZE; i++)
	{
		for (j = 0; j < PATTERN_SIZE; j++)
		{
			val = pattern->values[i][j];
			if (val < min) min = val;
			if (val > max) max = val;

		}
	}
	for (i = 0; i < PATTERN_SIZE; i++)
	{
		for (j = 0; j < PATTERN_SIZE; j++)
		{
			pattern->values[i][j] = (pattern->values[i][j] - min) / (max - min);
		}
	}
}

static void waveletTransform(Pattern *dst, Pattern *src, int size)
{
	if (size > 1)
	{
		int i, j;
		size /= 2;
		for (i = 0; i < size; i++)
		{
			for (j = 0; j < size; j++)
			{
				dst->values[i + size][j] =        ( - src->values[2 * i][2 * j]     + src->values[2 * i + 1][2 * j]
				                                    - src->values[2 * i][2 * j + 1] + src->values[2 * i + 1][2 * j + 1]) / 4.0f;
				dst->values[i][j + size] =        ( - src->values[2 * i][2 * j]     - src->values[2 * i + 1][2 * j]
				                                    + src->values[2 * i][2 * j + 1] + src->values[2 * i + 1][2 * j + 1]) / 4.0f;
				dst->values[i + size][j + size] = (   src->values[2 * i][2 * j]     - src->values[2 * i + 1][2 * j]
				                                    - src->values[2 * i][2 * j + 1] + src->values[2 * i + 1][2 * j + 1]) / 4.0f;
			}
		}
		for (i = 0; i < size; i++)
		{
			for (j = 0; j < size; j++)
			{
				src->values[i][j] =               (   src->values[2 * i][2 * j]     + src->values[2 * i + 1][2 * j]
				                                    + src->values[2 * i][2 * j + 1] + src->values[2 * i + 1][2 * j + 1]) / 4.0f;
			}
		}
		waveletTransform(dst, src, size);
	}
	else
	{
		dst->values[0][0] = src->values[0][0];
	}
}


static Pattern* image2pattern(gdImagePtr im, Pattern* pattern)
{
	gdImagePtr	tb;
	Pattern source;

	/* Resize image */
	tb = gdImageCreateTrueColor(PATTERN_SIZE, PATTERN_SIZE);
	if (!tb)
	{
		printf("Error creating pattern\n");
		return NULL;
	}
	gdImageCopyResampled(tb, im, 0, 0, 0, 0, PATTERN_SIZE, PATTERN_SIZE,
			im->sx, im->sy);

	/* Create source pattern as greyscale image */
	makePattern(tb, &source);
	gdImageDestroy(tb);

	/* "Normalize" intensiveness in the pattern */
	normalizePattern(&source);

	/* Do wavelet transform */
	waveletTransform(pattern, &source, PATTERN_SIZE);

	return pattern;
}

Pattern* jpeg2pattern(void* img, int size, Pattern * pattern)
{
	gdImagePtr im;

	im = gdImageCreateFromJpegPtr(size, img);
	if (!im)
	{
		printf("Error loading jpeg\n");
		return (Pattern*)NULL;
	}
	pattern = image2pattern(im, pattern);
	gdImageDestroy(im);

	return pattern;
}

Pattern* png2pattern(void* img, int size, Pattern* pattern)
{
	gdImagePtr im;

	im = gdImageCreateFromPngPtr(size, img);
	if (!im)
	{
		printf("Error loading png\n");
		return (Pattern*)NULL;
	}
	pattern = image2pattern(im, pattern);
	gdImageDestroy(im);

	return pattern;
}

Pattern* gif2pattern(void* img, int size, Pattern* pattern)
{
	gdImagePtr im;

	im = gdImageCreateFromGifPtr(size, img);
	if (!im)
	{
		printf("Error loading gif\n");
		return (Pattern*)NULL;
	}
	pattern = image2pattern(im, pattern);
	gdImageDestroy(im);

	return pattern;
}

Pattern* webp2pattern(void* img, int size, Pattern* pattern)
{
	gdImagePtr im;

	im = gdImageCreateFromWebpPtr(size, img);
	if (!im)
	{
		printf("Error loading webp\n");
		return (Pattern*)NULL;
	}
	pattern = image2pattern(im, pattern);
	gdImageDestroy(im);

	return pattern;
}


static float calcSumm(Pattern *pattern, int x, int y, int sX, int sY)
{
	int i, j;
	float summ = 0.0f, val;
	for (i = x; i < x + sX; i++)
	{
		for (j = y; j < y + sY; j++)
		{
			val = pattern->values[i][j];
			summ += val * val;
		}
	}
	return sqrt(summ);
}
