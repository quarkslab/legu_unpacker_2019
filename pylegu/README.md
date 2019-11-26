## PyLegu

Python bindings that expose the functions ``nrv_decompresss()`` and ``decrypt()``.

The ``nrv_decompresss()`` function is based on [UCL](http://www.oberhumer.com/opensource/ucl/) ``ucl_nrv2d_decompress()`` and the decrypt function is a slightly modified version of XTEA:

```cpp
int xtea_decrypt(uint32_t* key, uint32_t* buf, size_t ilen, size_t nb_round) {
  const size_t count = ilen / 8;
  const size_t key_off = (ilen & 8) / 4;
  static constexpr uint32_t DELTA = 0x9e3779b9;

  const uint32_t key_0 = key[key_off + 0];
  const uint32_t key_1 = key[key_off + 1];

  for (size_t i = 0; i < count * 2; i += 2) {
    buf[i + 0] ^= key_0;
    buf[i + 1] ^= key_1;

    uint32_t sum = DELTA * nb_round;
    uint32_t temp0 = buf[i + 0];
    uint32_t temp1 = buf[i + 1];

    for (size_t j = 0; j < nb_round; ++j) {
      temp1 -= (key[2] + (temp0 << 4)) ^ (key[3] + (temp0 >> 5)) ^ (temp0 + sum);
      temp0 -= (key[0] + (temp1 << 4)) ^ (key[1] + (temp1 >> 5)) ^ (temp1 + sum);
      sum -= DELTA;
    }
    buf[i + 0] = temp0;
    buf[i + 1] = temp1;
  }
  return 0;
}
```

To install the package:

```bash
$ python ./setup.py build -j4 install --user
# OR
$ python ./setup.py build -j4 develop --user
```

## Example

```python
import pylegu

# Decompression
compressed_buffer = XXX
uncompressed_size = 0x1000
uncompressed = pylegu.nrv_decompress(list(compressed_buffer), uncompressed_size)

# XTEA decryption
key = b"..."
nb_round = 3
encrypted_buffer = YYY
decrypted = pylegu.decrypt(list(ekey), list(encrypted_buffer), nb_round)
```
