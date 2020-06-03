# These tests are not for test vector suite, so it's okay to ues pytest

import pytest

from eth2spec.phase0 import spec as phase0_spec
from eth2spec.phase1 import spec as phase1_spec


all_specs = [phase0_spec, phase1_spec]


@pytest.mark.parametrize(
    ('spec'), all_specs
)
@pytest.mark.parametrize(
    ('value, output, success'),
    [
        (0, 0, True),
        (1, 1, True),
        (4, 2, True),
        (5, 2, True),
        (-1, None, False),  # underflow
    ]
)
def test_integer_squareroot(spec, value, output, success):
    if success:
        assert spec.integer_squareroot(value) == output
        assert output**2 <= value
    else:
        with pytest.raises(Exception):
            spec.integer_squareroot(value)


@pytest.mark.parametrize(
    ('spec'), all_specs
)
@pytest.mark.parametrize(
    ('bytes_1, bytes_2, output, success'),
    [
        (b'\xff' * 32, b'\x00' * 32, b'\xff' * 32, True),
        (b'\x0f' * 32, b'\xf0' * 32, b'\xff' * 32, True),
        (b'\xff' * 32, b'\x00' * 33, None, False),  # bytes_2 has wrong length
        (b'\xff' * 32, b'\x00' * 31, None, False),  # bytes_2 has wrong length
    ]
)
def test_xor(spec, bytes_1, bytes_2, output, success):
    if success:
        assert spec.xor(bytes_1, bytes_2) == output
    else:
        with pytest.raises(Exception):
            spec.xor(bytes_1, bytes_2)


@pytest.mark.parametrize(
    ('spec'), all_specs
)
@pytest.mark.parametrize(
    ('data, output, success'),
    [
        (b'\x01\x02\x03\x04', int.from_bytes(b'\x01\x02\x03\x04', 'little'), True),
        (b'\xff' * 8, 2**64 - 1, True),
        (b'\x00' * 8, 0, True),
        (b'', 0, True),
        (b'\xff' * 9, None, False),  # overflow
    ]
)
def test_bytes_to_int(spec, data, output, success):
    if success:
        result = spec.bytes_to_int(data)
        assert result == output
        assert result >= 0
    else:
        with pytest.raises(Exception):
            spec.bytes_to_int(data)
