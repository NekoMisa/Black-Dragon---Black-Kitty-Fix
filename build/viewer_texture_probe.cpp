#include "linden_common.h"
#include "llcommon.h"
#include "llimage.h"
#include "llimagej2c.h"
#include <fstream>
#include <iostream>
#include <iterator>

int main(int argc, char** argv)
{
    LLCommon::initClass();
    LLImage::initClass();
    int failures = 0;
    std::cout << LLImageJ2C::getEngineInfo() << std::endl;
    for (int a = 1; a < argc; ++a) {
        std::ifstream file(argv[a], std::ios::binary);
        std::vector<char> data((std::istreambuf_iterator<char>(file)), {});
        for (int partial : {1, 0}) {
            LLPointer<LLImageJ2C> encoded = new LLImageJ2C;
            int count = partial ? llmin(600, (int)data.size()) : (int)data.size();
            encoded->allocateData(count);
            memcpy(encoded->getData(), data.data(), count);
            bool metadata = encoded->updateData();
            encoded->setDiscardLevel(5);
            LLPointer<LLImageRaw> raw = new LLImageRaw;
            bool decoded = metadata && encoded->decode(raw, 0.f);
            bool okay = decoded && raw->getData() && raw->getWidth() == (encoded->getWidth()+31)/32
                        && raw->getHeight() == (encoded->getHeight()+31)/32;
            std::cout << "viewer partial=" << partial << " success=" << okay << " size="
                      << raw->getWidth() << 'x' << raw->getHeight() << std::endl;
            failures += !okay;
        }
    }
    for (int size : {16, 128}) {
        LLPointer<LLImageRaw> input = new LLImageRaw(size, size, 4);
        for (int i = 0; i < input->getDataSize(); ++i) input->getData()[i] = (i * 13) % 256;
        LLPointer<LLImageJ2C> encoded = new LLImageJ2C;
        encoded->setReversible(true);
        bool okay = encoded->encode(input, 0.f);
        encoded->setDiscardLevel(0);
        LLPointer<LLImageRaw> output = new LLImageRaw;
        okay = okay && encoded->decode(output, 0.f) && output->getDataSize() == input->getDataSize()
               && memcmp(input->getData(), output->getData(), input->getDataSize()) == 0;
        std::cout << "viewer lossless roundtrip " << size << " success=" << okay << std::endl;
        failures += !okay;
    }
    std::cout << "Failures: " << failures << std::endl;
    return failures ? 1 : 0;
}
