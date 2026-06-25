from loopfeature.point import Point

def test_access_attribute_class_Point():
    point1 = Point(10, 20, 123456789, 230)
    assert point1.latitude == 10
    assert point1.longitude == 20
    assert point1.id == 123456789
    assert point1.elevation == 230

def test_hashable_class_Point():
    point1 = Point(10, 20, 1234, 300)
    point2 = Point(20, 10, 5678, 150)
    
    dict_ = {point1:"point1", point2:"point2"}
    
    point3 = Point(10, 20, 1234, 300)

    assert dict_[point1] == dict_[point3]

def test_calcul_dist_Point():
    point1 = Point(0, 1, 1234, 2200)
    point2 = Point(0, 3, 5678, 8000)

    assert point1.calcul_dist(point2) == 222640.0 == point2.calcul_dist(point1)