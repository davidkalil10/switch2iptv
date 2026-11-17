import struct
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from verify_switch2_package import verify_aset, verify_link_map, verify_switch2_startup


def make_fake_nro(with_oun0: bool = True, with_aset: bool = True) -> bytes:
    buf = bytearray(0x2000)
    struct.pack_into("<I", buf, 4, 0x80)
    buf[0x10:0x14] = b"NRO0"
    mod = 0x80
    buf[mod : mod + 4] = b"MOD0"
    at = mod + 0x1C
    buf[at : at + 4] = b"LNY0"
    at += 12
    if with_oun0:
        buf[at : at + 4] = b"OUN0"
        struct.pack_into("<II", buf, at + 4, 2, 1)
    if with_aset:
        aset_off = 0x1000
        struct.pack_into("<I", buf, 0x18, aset_off)
        buf[aset_off : aset_off + 4] = b"ASET"
        icon_off = 0x38
        icon_size = 128
        nacp_off = icon_off + icon_size
        nacp_size = 0x4000
        buf.extend(b"\x00" * (aset_off + nacp_off + nacp_size - len(buf)))
        struct.pack_into("<QQ", buf, aset_off + 0x08, icon_off, icon_size)
        struct.pack_into("<QQ", buf, aset_off + 0x18, nacp_off, nacp_size)
        buf[aset_off + icon_off : aset_off + icon_off + 3] = b"\xff\xd8\xff"
    return bytes(buf)


class TestSwitch2Package(unittest.TestCase):
    def test_valid_nro(self):
        raw = make_fake_nro(with_oun0=True, with_aset=True)
        verify_switch2_startup(raw)
        verify_aset(raw)

    def test_missing_oun0(self):
        raw = make_fake_nro(with_oun0=False, with_aset=True)
        with self.assertRaises(ValueError):
            verify_switch2_startup(raw)

    def test_valid_link_map(self):
        verify_link_map(
            "/opt/devkitpro/libounce/lib/libnx.a\n"
            "/opt/devkitpro/portlibs/switch2/lib/libEGL.a\n"
            "build/switch2/ffmpeg-install/lib/libavcodec.a\n"
            "/opt/devkitpro/portlibs/switch/lib/libmpv.a\n"
        )

    def test_forbidden_switch1_link_map(self):
        with self.assertRaises(ValueError):
            verify_link_map(
                "/opt/devkitpro/libounce/lib/libnx.a\n"
                "/opt/devkitpro/portlibs/switch2/lib/libEGL.a\n"
                "/opt/devkitpro/portlibs/switch/lib/libavutil.a(hwcontext_nvtegra.o)\n"
            )


if __name__ == "__main__":
    unittest.main()
