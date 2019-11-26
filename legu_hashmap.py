# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class LeguHashmap(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.header = self._root.HeaderT(self._io, self, self._root)
        self.classes_info = [None] * (self.header.table_size)
        for i in range(self.header.table_size):
            self.classes_info[i] = self._root.ClassesInfoT(self._io, self, self._root)

        self.nb_methods_info = self._io.read_u4le()
        self.methods_info = [None] * (self.nb_methods_info)
        for i in range(self.nb_methods_info):
            self.methods_info[i] = self._root.MethodsInfoT(self._io, self, self._root)


    class HeaderT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.unknown = self._io.read_u4le()
            self.table_size = self._io.read_u4le()


    class ClassesInfoT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.utf8_hash = self._io.read_u4le()
            self.string_off = self._io.read_u4le()
            self.methods_info_idx = self._io.read_u4le()


    class MethodsInfoT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.nb_methods = self._io.read_u4le()
            self.packed_info = [None] * (self.nb_methods)
            for i in range(self.nb_methods):
                self.packed_info[i] = self._root.PackedMethodT(self._io, self, self._root)



    class PackedMethodT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.packed_code_off = self._io.read_u4le()
            self.code_size = self._io.read_u4le()
            self.code_off = self._io.read_u4le()



