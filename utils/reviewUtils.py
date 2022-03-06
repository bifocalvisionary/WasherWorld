"""
reviewUtils
Hendrick Ducasse

A utility for managing reviews
"""


class Review:
    def __init__(self, reviewID: int, rating: int, timeSubmitted, message: str):
        self.reviewID = reviewID
        self.rating = rating
        self.timeSubmitted = timeSubmitted
        self.message = message


def import_review_db(reviewTuple):
    return Review(reviewTuple[0], reviewTuple[1], reviewTuple[2], reviewTuple[3])