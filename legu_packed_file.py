# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class LeguPackedFile(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.nb_dex_files = self._io.read_u4le()
        self.packed_dex = [None] * (self.nb_dex_files)
        for i in range(self.nb_dex_files):
            self.packed_dex[i] = self._root.PackedDexT(self._io, self, self._root)

        self.hashmaps = [None] * (self.nb_dex_files)
        for i in range(self.nb_dex_files):
            self.hashmaps[i] = self._root.HashmapT(self._io, self, self._root)

        self.packed_bytecode = [None] * (self.nb_dex_files)
        for i in range(self.nb_dex_files):
            self.packed_bytecode[i] = self._root.PackedBytecodeT(self._io, self, self._root)


    class PackedDexT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.unknown1 = self._io.read_u8le()
            self.uncompressed_size = self._io.read_u4le()
            self.compressed_size = self._io.read_u4le()
            self.unknown2 = self._io.read_u4le()
            self.data = self._io.read_bytes(self.compressed_size)


    class HashmapT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.uncompressed_size = self._io.read_u4le()
            self.compressed_size = self._io.read_u4le()
            self.data = self._io.read_bytes(self.compressed_size)


    class PackedBytecodeT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.uncompressed_size = self._io.read_u4le()
            self.compressed_size = self._io.read_u4le()
            self.data = self._io.read_bytes(self.compressed_size)



