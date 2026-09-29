#include <stdio.h>
#include "openjpeg.h"

static void message(const char *s, void *unused) { fprintf(stderr, "%s", s); }
int main(int argc, char **argv)
{
    opj_dparameters_t params;
    opj_codec_t *codec;
    opj_stream_t *stream;
    opj_image_t *image = NULL;
    int okay;
    if (argc != 2) return 2;
    opj_set_default_decoder_parameters(&params);
    params.cp_reduce = 5;
    codec = opj_create_decompress(OPJ_CODEC_J2K);
    opj_set_error_handler(codec, message, NULL);
    opj_setup_decoder(codec, &params);
    opj_decoder_set_strict_mode(codec, OPJ_FALSE);
    stream = opj_stream_create_default_file_stream(argv[1], OPJ_TRUE);
    okay = stream && opj_read_header(stream, codec, &image) && opj_decode(codec, stream, image);
    if (okay && image && image->numcomps && image->comps[0].data)
        printf("decoded=%ux%u components=%u factor=%u\n", image->comps[0].w, image->comps[0].h, image->numcomps, image->comps[0].factor);
    else { puts("DECODE FAILED"); okay = 0; }
    if (image) opj_image_destroy(image);
    if (stream) opj_stream_destroy(stream);
    opj_destroy_codec(codec);
    return okay ? 0 : 1;
}
