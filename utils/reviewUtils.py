"""
reviewUtils
Hendrick Ducasse

A utility for managing reviews
"""


class Review:
    def __init__(self, reviewNum: int, rating: int, timeSubmitted, message: str):
        self.reviewNum = int
        self.rating = rating
        self.timeSubmitted = timeSubmitted
        self.message = message
