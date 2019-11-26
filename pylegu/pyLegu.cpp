#include "pyLegu.hpp"
#include <ucl/ucl.h>
#include <ucl/uclconf.h>

namespace py = pybind11;
using namespace py::literals;

int xtea(uint32_t* key, uint32_t* buf, size_t ilen, size_t nb_round) {
  const size_t count = ilen / 8;
  const size_t key_off = (ilen & 8) / 4;
  static constexpr uint32_t DELTA = 0x9e3779b9;

  if (key == nullptr) {
    py::print("key is null!");
    return -1;
  }

  if (ilen % 4 != 0) {
    py::print("Buffer not aligned");
    return -1;
  }

  if (nb_round == 0) {
    py::print("Number of round must be greater than 0");
    return -1;
  }

  const uint32_t key_0 = key[key_off + 0];
  const uint32_t key_1 = key[key_off + 1];

  for (size_t i = 0; i < count * 2; i += 2) {
    buf[i + 0] ^= key_0;
    buf[i + 1] ^= key_1;

    uint32_t magic = DELTA * nb_round;
    uint32_t temp0 = buf[i + 0];
    uint32_t temp1 = buf[i + 1];

    for (size_t j = 0; j < nb_round; ++j) {
      temp1 -= (key[2] + (temp0 << 4)) ^ (key[3] + (temp0 >> 5)) ^ (temp0 + magic);
      temp0 -= (key[0] + (temp1 << 4)) ^ (key[1] + (temp1 >> 5)) ^ (temp1 + magic);
      magic -= DELTA;
    }
    buf[i + 0] = temp0;
    buf[i + 1] = temp1;
  }
  return 0;
}

py::module legu_module("pylegu", "Low level bindings used to unpack Legu");
PYBIND11_MODULE(pylegu, legu_module) {

  legu_module.def("ucl_version_string",
    ucl_version_string);

  legu_module.def("ucl_version_date",
    ucl_version_date);

  int ret = UCL_E_OK;
  if ((ret = ucl_init()) != UCL_E_OK) {
    py::print("ucl_init() failed: " + std::to_string(ret));
  }

  legu_module.def(
      "decrypt",
      [] (std::vector<uint8_t> key, const std::vector<uint8_t>& inbuffer, size_t nround) {
        std::vector<uint8_t> dst = inbuffer;
        xtea(reinterpret_cast<uint32_t*>(key.data()), reinterpret_cast<uint32_t*>(dst.data()), dst.size(), nround);
        return dst;
      });

  legu_module.def(
      "nrv_decompress",
      [] (std::vector<uint8_t> src, size_t olen) {
        std::vector<uint8_t> dst(olen, 0);
        uint32_t size = olen;
        int res = ucl_nrv2d_decompress_safe_8(
            src.data(), src.size(),
            dst.data(), &size,
            nullptr);

        if (res != UCL_E_OK) {
          py::print("[-] Decompression finished with error: {:d}"_s.format(res));
        }

        return dst;
      });
}
