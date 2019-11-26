meta:
  id: legu_hashmap
  title: Structure of the hashmap used by Tencent Legu packer
  endian: le
seq:
  - id: header
    type: header_t
  - id: classes_info
    type: classes_info_t
    repeat: expr
    repeat-expr: header.table_size
  - id: nb_methods_info
    type: u4
  - id: methods_info
    type: methods_info_t
    repeat: expr
    repeat-expr: nb_methods_info
types:
  header_t:
    seq:
      - id: unknown
        type: u4
      - id: table_size
        type: u4
        doc: |
          Number of element in the hashmap
  classes_info_t:
    seq:
      - id: utf8_hash
        type: u4
        doc: |
          Class's name hash value
        doc-ref: http://androidxref.com/4.4.4_r1/xref/dalvik/vm/UtfString.cpp#88
      - id: string_off
        type: u4
        doc: |
          Offset in the original DEX file of the class's name associated with this index
      - id: methods_info_idx
        type: u4
        doc: |
          Index of packed methods information in the 'methods_info' field
  methods_info_t:
    seq:
      - id: nb_methods
        type: u4
        doc: |
          Number of methods associated with this entry
      - id: packed_info
        type: packed_method_t
        repeat: expr
        repeat-expr: nb_methods
        doc: |
          Information about the packed methods
  packed_method_t:
    seq:
      - id: packed_code_off
        type: u4
        doc: |
          Offset into the Legu packed data
      - id: code_size
        type: u4
        doc: |
          Code size of the method
      - id: code_off
        type: u4
        doc: |
          Offset of the Davik bytecode in the original DEX file
