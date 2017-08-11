import pytest

import numpy as np

from traitlets import HasTraits, Instance, Undefined
from ipywidgets import Widget, widget_serialization

from ..ndarray.union import DataUnion
from ..ndarray.serializers import (
    data_union_from_json, data_union_to_json,
    array_from_json, array_to_json
)


def test_array_from_json_correct_data():
    raw_data = memoryview(np.zeros((4, 3), dtype=np.float32))
    json_data = {
        'buffer': raw_data,
        'dtype': 'float32',
        'shape': [4, 3],
    }
    data = array_from_json(json_data, None)
    # Note: We simply use None for the widget parameter since
    # we currently don't use it. Tests should be updated in the
    # future if it is later needed.

    np.testing.assert_equal(raw_data, data)

def test_array_from_json_none():
    assert array_from_json(None, None) is None


def test_array_to_json_correct_data():
    data = np.zeros((4, 3), dtype=np.float32)
    json_data = array_to_json(data, None)

    assert json_data == {
        'buffer': memoryview(data),
        'dtype': str(data.dtype),
        'shape': (4, 3),
    }

def test_array_to_json_none():
    assert array_to_json(None, None) is None

def test_array_to_json_continuous_data():
    data = np.zeros((4, 3), dtype=np.float32, order='F')
    json_data = array_to_json(data, None)

    reinterpreted_data = array_from_json(json_data, None)
    np.testing.assert_equal(data, reinterpreted_data)
    assert reinterpreted_data.flags['C_CONTIGUOUS']



def test_union_from_json_correct_array_data():
    raw_data = memoryview(np.zeros((4, 3), dtype=np.float32))
    json_data = {
        'buffer': raw_data,
        'dtype': 'float32',
        'shape': [4, 3],
    }

    data = data_union_from_json(json_data, None)
    np.testing.assert_equal(raw_data, data)

def test_union_from_json_correct_widget_data():
    dummy = Widget()

    json_data = widget_serialization['to_json'](dummy, None)

    data = data_union_from_json(json_data, None)
    assert data == dummy

def test_union_from_json_none():
    assert data_union_from_json(None, None) is None


def test_union_to_json_correct_array_data():
    data = np.zeros((4, 3), dtype=np.float32)
    json_data = data_union_to_json(data, None)

    assert json_data == {
        'buffer': memoryview(data),
        'dtype': str(data.dtype),
        'shape': (4, 3),
    }

def test_union_to_json_correct_widget_data():
    dummy = Widget()
    json_data = data_union_to_json(dummy, None)

    assert json_data == widget_serialization['to_json'](dummy, None)

def test_union_to_json_none():
    assert data_union_to_json(None, None) is None
