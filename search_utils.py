def manhattan_distance(point1, point2):
    p1x, p1y = point1
    p2x, p2y = point2
    return abs(p1x - p2x) + abs(p1y - p2y)


def euclidean_distance(point1, point2):
    p1x, p1y = point1
    p2x, p2y = point2
    return ((p1x - p2x) ** 2 + (p1y - p2y) ** 2) ** 0.5
