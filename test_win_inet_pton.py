import pytest
import socket
import sys


INET_PTON = []
INET_NTOP = []


orig_inet_pton = getattr(socket, "inet_pton", None)
orig_inet_ntop = getattr(socket, "inet_ntop", None)

if orig_inet_ntop:
    INET_NTOP.append(orig_inet_ntop)
if orig_inet_pton:
    INET_PTON.append(orig_inet_pton)


import win_inet_pton

win_inet_pton.inject_into_socket()

INET_PTON.append(orig_inet_pton)
INET_NTOP.append(orig_inet_ntop)


VALID_IP_ADDRESSES = [
    (socket.AF_INET, "0.0.0.0", b"\x00\x00\x00\x00"),
    (socket.AF_INET, "1.2.3.4", b"\x01\x02\x03\x04"),
    (socket.AF_INET, "255.254.253.252", b"\xff\xfe\xfd\xfc"),
    (socket.AF_INET, "127.0.0.1", b"\x7f\x00\x00\x01"),
    (
        socket.AF_INET6,
        "::",
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
    ),
    (
        socket.AF_INET6,
        "::1",
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01",
    ),
    (
        socket.AF_INET6,
        "1::ABCD:ffFf",
        b"\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xab\xcd\xff\xff",
    ),
]
INVALID_IP_ADDRESSES = [
    (socket.AF_INET, "1.1.1."),
    (socket.AF_INET, ".1.1.1"),
    (socket.AF_INET, "1.1"),
    (socket.AF_INET, "256.1.1.1"),
    (socket.AF_INET, "-1.1.1.1"),
    (socket.AF_INET, "1.-1.1.1"),
    (socket.AF_INET, "::1"),
    (socket.AF_INET, "localhost"),
    (socket.AF_INET6, ":::1"),
    (socket.AF_INET6, ":1"),
    (socket.AF_INET6, "1::ffff1"),
    (socket.AF_INET6, "1.2.3.4"),
    (socket.AF_INET6, "localhost"),
]

INVALID_PACKED_ADDRESSES = [
    (socket.AF_INET, b"\x00\x00\x00"),
    (socket.AF_INET, b"\x00\x00\x00\x00\x00"),
    (
        socket.AF_INET6,
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
    ),
    (
        socket.AF_INET6,
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
    ),
]


@pytest.fixture(params=INET_NTOP)
def inet_ntop(request):
    return request.param


@pytest.fixture(params=INET_PTON)
def inet_pton(request):
    return request.param


@pytest.mark.parametrize(["family", "address", "packed"], VALID_IP_ADDRESSES)
def test_valid_ip_addresses(inet_pton, inet_ntop, family, address, packed):
    assert inet_pton(family, address) == packed
    assert inet_ntop(family, packed) == address.lower()


@pytest.mark.parametrize(["family", "address"], INVALID_IP_ADDRESSES)
def test_invalid_ip_addresses(inet_pton, family, address):
    with pytest.raises(socket.error):
        inet_pton(family, address)


@pytest.mark.parametrize(["family", "packed"], INVALID_PACKED_ADDRESSES)
def test_invalid_packed_addresses(inet_ntop, family, packed):
    with pytest.raises(ValueError):
        inet_ntop(family, packed)


@pytest.mark.parametrize(["family", "address", "packed"], VALID_IP_ADDRESSES)
def test_unknown_family(inet_pton, inet_ntop, family, address, packed):
    with pytest.raises(ValueError):
        inet_ntop(1000, packed)
    with pytest.raises(OSError):
        inet_pton(1000, address)


@pytest.mark.parametrize(["family", "address", "packed"], VALID_IP_ADDRESSES)
def test_valid_ip_addresses_unicode(inet_pton, inet_ntop, family, address, packed):
    if sys.version_info[0] == 3:
        with pytest.raises(TypeError):
            inet_pton(family, address.encode("ascii"))
        with pytest.raises(TypeError):
            inet_ntop(family, ''.join(chr(x) for x in packed))
    else:
        assert inet_pton(family, address.decode("ascii")) == packed
        assert inet_ntop(family, packed.decode("ascii")) == address.lower()
