from loopfeature.segment import Segment

def test_access_attribute_Segment():
    segment = Segment(35, 123456789, (45, 1), (46, 2), 36, 10, 400, False)
    assert segment.id == 123456789
    assert segment.score == 35
    assert segment.first_point == (45, 1)
    assert segment.last_point == (46, 2)
    assert segment.elev_gain_FtoL == 36
    assert segment.elev_gain_LtoF == 10
    assert segment.distance == 400
    assert not segment.is_service