from loopfeature.segment import Segment

def test_access_attribute_Segment():
    segment = Segment(35, 29, 123456789)
    assert segment.id == 123456789
    assert segment.ratio == 29
    assert segment.value == 35
