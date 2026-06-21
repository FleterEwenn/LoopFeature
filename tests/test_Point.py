from loopfeature.point import Point

def test_access_attribute_class_Point():
    point1 = Point(10, 20)
    assert point1.latitude == 20
    assert point1.longitude == 10

def test_hashable_class_Point():
    point1 = Point(10, 20)
    point2 = Point(20, 10)
    
    dict_ = {point1:"point1", point2:"point2"}
    
    point3 = Point(10, 20)

    assert dict_[point1] == dict_[point3]