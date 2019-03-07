# metres_between calculates and returns the metres between point_a and
# point_b where each point is a 2-element list [longitude, latitude]
# or a 2-tuple (longitude, latitude).
#
# Adapted from https://rosettacode.org/wiki/Haversine_formula#Python
def metres_between(point_a, point_b):
    R = 6372.8 # Earth radius in kilometers

    delta_lat = math.radians(point_b[1] - point_a[1])
    delta_lon = math.radians(point_b[0] - point_a[0])
    point_a1 = math.radians(point_a[1])
    point_b1 = math.radians(point_b[1])
   
    a = (math.sin(delta_lat/2)**2 +
         math.cos(point_a1) * math.cos(point_b1) * math.sin(delta_lon/2)**2)
    c = 2 * math.asin(math.sqrt(a))

    return R * c * 1000.0