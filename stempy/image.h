#ifndef stempyimages_h
#define stempyimages_h

#include "reader.h"

#include <vector>
#include <memory>


namespace stempy {

  struct Image {
    std::shared_ptr<uint64_t[]> data;
    uint32_t width = 0;
    uint32_t height = 0;

    Image() = default;
    Image(uint32_t width, uint32_t height);
    Image(Image&& i) noexcept = default;
    Image& operator=(Image&& i) noexcept = default;
  };

  struct STEMValues {
    uint64_t bright = 0;
    uint64_t dark = 0;
    uint32_t imageNumber = -1;
  };

  struct STEMImage {
    Image bright;
    Image dark;

    STEMImage() = default;
    STEMImage(uint32_t width, uint32_t height);
    STEMImage(STEMImage&& i) noexcept = default;
    STEMImage& operator=(STEMImage&& i) noexcept = default;
  };

  struct DarkFieldReference {
    std::shared_ptr<uint64_t[]> referenceFrame;
    uint32_t size = 0;
    float mean;
    float variance;

    DarkFieldReference() = default;
    DarkFieldReference(uint32_t size);
    DarkFieldReference(DarkFieldReference&& d) noexcept = default;
    DarkFieldReference& operator=(DarkFieldReference&& d) noexcept = default;
  };

  STEMImage createSTEMImage(std::vector<Block> &blocks, int rows, int colums,  int innerRadius, int outerRadius);
  STEMValues calculateSTEMValues(uint16_t data[], int offset,
                                 int numberOfPixels,
                                 uint16_t brightFieldMask[],
                                 uint16_t darkFieldMask[],
                                 uint32_t imageNumber=-1);

  DarkFieldReference createDarkFieldReference(std::vector<Block>& blocks, int rows, int columns,
      int numberOfSamples=20, int upperLimit=5, int sampleStripWidth=100);
}

#endif
