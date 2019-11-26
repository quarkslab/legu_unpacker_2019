#!/usr/bin/env python
#################################################
# Description:
# Script to unpack APK protected by Tencent Legu.
# The APK protected by this packer are likely
# to embed libshell-super.2019.so and libshella-4.1.0.XY.so
#
# Author: Romain Thomas - @rh0main
#################################################
import sys
import argparse
from itertools import cycle
import lief
import io
from typing import Optional
import zipfile
import re

import pylegu
from legu_hashmap import LeguHashmap
from legu_packed_file import LeguPackedFile


_LIBSHELL_RE = re.compile(r"libshell\w-([\d\.]+).so")
MASK32 = (1 << 32) - 1

SUPPORTED_VERSION = {"4.1.0.15", "4.1.0.18"}

KEY  = b"^hHc7Ql]N9Z4:+1m~nTcA&3a7|?GB1z@"
""" Hard coded key located in the native library libshell-super.2019.so """

def key_derivation(key: bytes) -> bytes:
    """
    Routine to derive the decryption key used in XTEA
    """
    return bytes(x1 ^ x2 for x1, x2 in zip(KEY, cycle(key)))

def decrypt(buff: bytes, password: bytes) -> bytes:
    """
    Decrypt the buffer with XTEA
    """
    limit = len(buff) & 0xFFFFFFF8
    aligned_buff = buff[:limit]
    ekey = key_derivation(password)
    nb_round = 3
    uncrypted = pylegu.decrypt(list(ekey), list(aligned_buff), nb_round)
    uncrypted += buff[limit:]
    return bytes(uncrypted)


def dvmComputeUtf8Hash(clazz: str) -> int:
    """
    Ref: http://androidxref.com/4.4.4_r1/xref/dalvik/vm/UtfString.cpp#88
    """
    h = 1
    for c in clazz:
        h = (((h * 31) & MASK32) + ord(c)) & MASK32
    return h


def get_class_info(hashmap: LeguHashmap, clazz: str) -> Optional[LeguHashmap.ClassesInfoT]:
    h = dvmComputeUtf8Hash(clazz)
    table_size = hashmap.header.table_size
    for i in range(table_size):
        table_idx = (h % table_size + i) % table_size
        entry = hashmap.classes_info[table_idx]
        if entry.utf8_hash != h:
            continue
        return entry
    return None


def should_process(cls: lief.DEX.Class) -> bool:
    return len(cls.methods) > 0 and any(len(m.bytecode) > 0 for m in cls.methods) and len(cls.fullname) > 1


def should_process_method(meth: lief.DEX.Method) -> bool:
    return meth.code_offset > 0 and len(meth.bytecode) > 0


def legu_unpack(apk_path: str):
    """
    Unpacking routine
    """
    with zipfile.ZipFile(apk_path) as zf:
        found = False
        for f in zf.namelist():
            matches = _LIBSHELL_RE.findall(f)
            if matches:
                found = True
                version = matches[0]
                print(f"[+] Legu version: {version}")
                if version not in SUPPORTED_VERSION:
                    print(f"[*] /!\ This version may not be supported!")
                break

        if not found:
            print("Unable to get the packer's version")
            sys.exit(1)

        # Contain the password to decrypt the hashmaps and the Dalvik bytecode
        with zf.open('assets/tosversion') as tosversion_fd:
            tosversion = tosversion_fd.read()
            password = tosversion[:16]

        # Packed data: dex files + hashmap + dalvik bytecode
        with zf.open('assets/0OO00l111l1l') as legu_fd:
            legu_data = legu_fd.read()

    print("[+] Password is '{}'".format(password.decode("utf8")))

    legu_main_data = LeguPackedFile.from_bytes(legu_data)

    print(f"[+] Number of dex files: {legu_main_data.nb_dex_files}")

    print(f"[+] Unpacking #{legu_main_data.nb_dex_files:d} DEX files ...")
    uncompressed_dex_files = list()
    hasmaps                = list()
    packed_methods_files   = list()

    for idx, packed_dex in enumerate(legu_main_data.packed_dex):
        print(f"[+] dex {idx:d} compressed size:   0x{packed_dex.compressed_size:x}")
        print(f"[+] dex {idx:d} uncompressed size: 0x{packed_dex.uncompressed_size:x}")
        uncompressed = pylegu.nrv_decompress(list(packed_dex.data), packed_dex.uncompressed_size + 0x400)
        uncompressed_dex_files.append(io.BytesIO(bytes(uncompressed)[0x10:]))

    print(f"\n[+] Unpacking #{legu_main_data.nb_dex_files:d} hashmap ...")
    for idx, hashmap in enumerate(legu_main_data.hashmaps):
        print(f"[+] hashmap {idx:d} compressed size:   0x{hashmap.compressed_size:x}")
        print(f"[+] hashmap {idx:d} uncompressed size: 0x{hashmap.uncompressed_size:x}")
        uncrypted = decrypt(hashmap.data, password)
        uncompressed = pylegu.nrv_decompress(list(uncrypted), hashmap.uncompressed_size + 0x400)
        hasmaps.append(io.BytesIO(bytes(uncompressed)))

    print(f"\n[+] Unpacking #{legu_main_data.nb_dex_files:d} packed methods ...")
    for idx, packedmethods in enumerate(legu_main_data.packed_bytecode):
        print(f"[+] packed methods {idx:d} compressed_size:   0x{packedmethods.compressed_size:x}")
        print(f"[+] packed methods {idx:d} uncompressed_size: 0x{packedmethods.uncompressed_size:x}")
        uncrypted = decrypt(packedmethods.data, password)
        uncompressed = pylegu.nrv_decompress(list(uncrypted), packedmethods.uncompressed_size + 0x400)
        packed_methods_files.append(io.BytesIO(bytes(uncompressed)))

    print("\n[+] Stage 2: Patching DEX files")
    for idx in range(legu_main_data.nb_dex_files):
        unpacked_dex        = uncompressed_dex_files[idx]
        packed_methods_data = packed_methods_files[idx]
        hashmap             = hasmaps[idx]

        hashmap = LeguHashmap.from_io(hashmap)
        dex = lief.DEX.parse(list(unpacked_dex.read()))

        for cls in filter(should_process, dex.classes):
            clazz = cls.fullname

            class_info = get_class_info(hashmap, clazz)
            if class_info is None:
                print(f"[-] KO for {clazz}")
                continue

            if class_info.methods_info_idx > hashmap.nb_methods_info:
                print(f"[-] KO for {clazz}")
                continue
            methods_info = hashmap.methods_info[class_info.methods_info_idx]

            assert methods_info.nb_methods == len([m for m in cls.methods if len(m.bytecode) > 0])

            for idx_meth, m in enumerate(filter(should_process_method, cls.methods)):
                packed_info = methods_info.packed_info[idx_meth]
                assert packed_info.code_size == len(m.bytecode)
                assert packed_info.code_off  == m.code_offset

                packed_methods_data.seek(packed_info.packed_code_off)
                code = packed_methods_data.read(packed_info.code_size)

                unpacked_dex.seek(m.code_offset)
                unpacked_dex.write(code)

    with zipfile.ZipFile('unpacked.apk', 'w') as zf:
        for idx in range(legu_main_data.nb_dex_files):
            unpacked_dex = uncompressed_dex_files[idx]
            unpacked_dex.seek(0)
            idx_dex = str(idx + 1) if idx > 0 else ""
            unpacked_path = f"classes{idx_dex}.dex"
            with zf.open(unpacked_path, "w") as zclasses:
                zclasses.write(unpacked_dex.read())

    print("[+] Unpacked APK: unpacked.apk")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Legu/Tencent unpacker')
    parser.add_argument('apk', help='Path to the packed APK')

    args = parser.parse_args()
    legu_unpack(args.apk)
