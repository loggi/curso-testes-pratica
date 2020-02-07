# coding: utf-8

DRIVER_APP_GEOFENCE_DISTANCE_MOTORCYCLE_DEFAULT = 600.0
DRIVER_APP_GEOFENCE_DISTANCE_DEFAULT = 743.59
DRIVER_APP_GEOFENCE_DISTANCE_VAN = 1500.0

TRANSPORT_TYPE_MOTORCYCLE = 'motocycle'
TRANSPORT_TYPE_BICYCLE = 'bike'
TRANSPORT_TYPE_VAN = 'van'
TRANSPORT_TYPE_CAR = 'car'


def get_checkin_geofence_radius(transport_type):
    """
    Get the radius in meters of checkin geofence by driver transport type
    :param transport_type: the driver transport type
    :return: radius in meters
    """

    if transport_type == TRANSPORT_TYPE_MOTORCYCLE:
        return DRIVER_APP_GEOFENCE_DISTANCE_MOTORCYCLE_DEFAULT
    elif transport_type == TRANSPORT_TYPE_VAN:
        return DRIVER_APP_GEOFENCE_DISTANCE_VAN
    else:
        return DRIVER_APP_GEOFENCE_DISTANCE_DEFAULT
