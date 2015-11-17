# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class hotelReview(Item):
    # define the fields for your item here like:
    # name = Field()
    # hotel profile

    hotel_name = Field()
    e_name = Field()
    avg_price = Field()
    url = Field()
    total_overall_rating = Field()
    avg_location = Field()
    avg_facility = Field()
    avg_service = Field()
    avg_clean = Field()
    all_comment = Field()
    recomment = Field()
    no_recomment = Field()

    # review
    author = Field()
    user_type = Field()
    date = Field()
    room_type = Field()
    review_overall_rating = Field()
    location = Field()
    facility = Field()
    service = Field()
    clean = Field()
    review = Field()
    helpful = Field()
