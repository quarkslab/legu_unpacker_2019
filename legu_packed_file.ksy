meta:
  id: legu_packed_file
  endian: le
seq:
  - id: nb_dex_files
    type: u4
    doc: |
      Number of orginal DEX files
  - id: packed_dex
    type: packed_dex_t
    repeat: expr
    repeat-expr: nb_dex_files
    doc: |
      Compressed DEX files (with NRV)
    doc-ref: http://www.oberhumer.com/products/nrv/
  - id: hashmaps
    type: hashmap_t
    repeat: expr
    repeat-expr: nb_dex_files
    doc: |
      Legu's hashmap associated with the packed DEX files (XTEA over NRV)
  - id: packed_bytecode
    type: packed_bytecode_t
    repeat: expr
    repeat-expr: nb_dex_files
    doc: |
      Packed Dalvik bytecode (XTEA over NRV)
types:
  packed_dex_t:
    seq:
      - id: unknown1
        type: u8
      - id: uncompressed_size
        type: u4
      - id: compressed_size
        type: u4
      - id: unknown2
        type: u4
      - id: data
        size: compressed_size
  hashmap_t:
    seq:
      - id: uncompressed_size
        type: u4
      - id: compressed_size
        type: u4
      - id: data
        size: compressed_size
  packed_bytecode_t:
    seq:
      - id: uncompressed_size
        type: u4
      - id: compressed_size
        type: u4
      - id: data
        size: compressed_size
