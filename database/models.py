import datetime
from .db import db
from flask_bcrypt import generate_password_hash, check_password_hash


class VisitingCard(db.Document):
    card_id = db.SequenceField()
    user_name = db.StringField(required=True, min_length=1, max_length=200)
    email = db.EmailField(required=True)
    mobile_no = db.StringField(required=True, min_length=10, max_length=10)
    company_name = db.StringField(required=False, min_length=1, max_length=200)
    designation = db.StringField(required=False, min_length=1, max_length=200)
    company_link = db.StringField(required=False, min_length=5, max_length=200)
    company_address = db.StringField(required=False, max_length=200)
    services_provided = db.StringField(required=False, max_length=200)
    facebook_link = db.StringField(required=False, min_length=5, max_length=200)
    messenger_link = db.StringField(required=False, min_length=5, max_length=200)
    twitter_link = db.StringField(required=False, min_length=5, max_length=200)
    linkedin_link = db.StringField(required=False, min_length=5, max_length=200)
    instagram_link = db.StringField(required=False, min_length=5, max_length=200)
    youtube_link = db.StringField(required=False, min_length=5, max_length=200)
    payment_link = db.StringField(required=False, min_length=5, max_length=200)
    other_payment_link = db.StringField(required=False, min_length=5, max_length=200)
    google_map_link = db.StringField(required=False, min_length=5, max_length=200)
    added_by = db.ReferenceField('User')
    created = db.DateTimeField(default=datetime.datetime.utcnow)


class Movie(db.Document):
    name = db.StringField(required=True, unique=True)
    casts = db.ListField(db.StringField(), required=True)
    genres = db.ListField(db.StringField(), required=True)
    added_by = db.ReferenceField('User')


class EventDetail(db.Document):
    event_id = db.SequenceField()
    bride_name = db.StringField(required=True, min_length=1, max_length=20)
    groom_name = db.StringField(required=True, min_length=1, max_length=20)
    mobile_no = db.StringField(required=True, min_length=10, max_length=10, unique=True)
    event_date = db.DateTimeField(required=True)
    venue = db.StringField(required=True, min_length=1, max_length=20)
    venue_address = db.StringField(required=True, min_length=1, max_length=200)
    added_by = db.ReferenceField('User')
    created = db.DateTimeField(default=datetime.datetime.utcnow)


class ImageDetail(db.Document):
    image_seq_id = db.SequenceField()
    image_ref_id = db.StringField(required=True,
                                  unique=True)  # from user and event_detail model image_ref_id will be assigned to this for reference
    image_data = db.ImageField(size=(300, 300, True), thumbnail_size=(150, 150, True))


class User(db.Document):
    user_id = db.SequenceField()  # sequence number
    email = db.EmailField(required=True, unique=True)
    user_name = db.StringField(required=False, min_length=1)
    picture_link = db.StringField(required=False, min_length=1)
    mobile_no = db.StringField(required=False, min_length=10, max_length=10)
    password = db.StringField(required=False, min_length=6)
    access_token= db.StringField(required=False, min_length=6)
    movies = db.ListField(db.ReferenceField('Movie', reverse_delete_rule=db.PULL))
    event_detail = db.ReferenceField('EventDetail', reverse_delete_rule=db.PULL)
    visiting_card = db.ReferenceField('VisitingCard', reverse_delete_rule=db.PULL)

    def hash_password(self):
        if not (self.password and self.password.strip()):
            self.password = "default"
            self.password = generate_password_hash(self.password).decode('utf8')
        else:
            self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)


User.register_delete_rule(Movie, 'added_by', db.CASCADE)
User.register_delete_rule(EventDetail, 'added_by', db.CASCADE)
