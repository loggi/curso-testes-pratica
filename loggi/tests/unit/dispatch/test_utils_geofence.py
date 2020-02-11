# coding: utf-8
from __future__ import absolute_import, unicode_literals
import pytest

from dispatch.utils import (
    DRIVER_APP_GEOFENCE_DISTANCE_MOTORCYCLE_DEFAULT,
    DRIVER_APP_GEOFENCE_DISTANCE_DEFAULT,
    DRIVER_APP_GEOFENCE_DISTANCE_VAN,
    TRANSPORT_TYPE_MOTORCYCLE,
    TRANSPORT_TYPE_BICYCLE,
    TRANSPORT_TYPE_VAN,
    TRANSPORT_TYPE_CAR
)

from dispatch.utils import get_checkin_geofence_radius


@pytest.mark.parametrize(
    'trasporte_type,expected',
    [(TRANSPORT_TYPE_MOTORCYCLE, DRIVER_APP_GEOFENCE_DISTANCE_MOTORCYCLE_DEFAULT),
     (TRANSPORT_TYPE_BICYCLE, DRIVER_APP_GEOFENCE_DISTANCE_DEFAULT),
     (TRANSPORT_TYPE_VAN, DRIVER_APP_GEOFENCE_DISTANCE_VAN),
     (TRANSPORT_TYPE_CAR, DRIVER_APP_GEOFENCE_DISTANCE_DEFAULT)
     ])
def test_get_checkin_geofence_radius(trasporte_type, expected):
    radius = get_checkin_geofence_radius(trasporte_type)
    assert radius == expected
