from .movie import MoviesApi, MovieApi
from .event_detail import EventDetailsApi, EventDetailApi
from .image_detail import DisplayImageApi, UploadImageApi
from .auth import SignupApi, LoginApi, LogoutApi, SocialAuthApi
from .reset_password import ForgotPassword, ResetPassword
from .visiting_card import VisitingCardsApi, VisitingCardApi


def initialize_routes(api):
    api.add_resource(MoviesApi, '/movies')
    api.add_resource(MovieApi, '/movies/<id>')

    api.add_resource(EventDetailsApi, '/event_details')
    api.add_resource(EventDetailApi, '/event_details/<id>')

    api.add_resource(VisitingCardsApi, '/visiting_cards')
    api.add_resource(VisitingCardApi, '/visiting_card/<id>')

    api.add_resource(UploadImageApi, '/upload_image')
    api.add_resource(DisplayImageApi, '/display_image/<id>')

    api.add_resource(SocialAuthApi, '/auth/socialauth')

    api.add_resource(SignupApi, '/auth/signup')
    api.add_resource(LoginApi, '/auth/login')
    api.add_resource(LogoutApi, '/auth/logout')

    api.add_resource(ForgotPassword, '/auth/forgot')
    api.add_resource(ResetPassword, '/auth/reset')
