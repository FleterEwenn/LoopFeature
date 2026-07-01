class Segment:
    def __init__(self, value:float, id:int, first_point, last_point, elev_gain_FtoL:float, elev_gain_LtoF:float, distance:float, is_service:bool):
        self.score = value
        self.id = id
        self.first_point = first_point
        self.last_point = last_point
        self.elev_gain_FtoL = elev_gain_FtoL
        self.elev_gain_LtoF = elev_gain_LtoF
        self.distance = distance
        self.is_service = is_service