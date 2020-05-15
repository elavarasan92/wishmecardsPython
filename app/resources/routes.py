from .movie import MoviesApi, MovieApi
from .event_detail import EventDetailsApi, EventDetailApi
from .image_detail import DisplayImageApi, UploadImageApi
from .auth import SignupApi, LoginApi, LogoutApi, SocialAuthApi, UserApi, UsersApi
from .render_html import RenderHTMLApi, BusinessCardApi, ShowCardApi
from .reset_password import ForgotPassword, ResetPassword
from .visiting_card import VisitingCardsApi, VisitingCardApi, VisitingCardViewApi


def initialize_routes(api):
    api.add_resource(MoviesApi, '/movies')
    api.add_resource(MovieApi, '/movies/<id>')
    api.add_resource(UsersApi, '/users')
    api.add_resource(UserApi, '/user_get_edit/<id>')

    api.add_resource(EventDetailsApi, '/event_details')
    api.add_resource(EventDetailApi, '/event_details/<id>')

    api.add_resource(VisitingCardsApi, '/visiting_cards')
    api.add_resource(VisitingCardApi, '/visiting_card/<id>')
    api.add_resource(VisitingCardViewApi, '/view_card/<user_name>')


    api.add_resource(UploadImageApi, '/upload_image/<id>')
    api.add_resource(DisplayImageApi, '/display_image/<id>')

    api.add_resource(SocialAuthApi, '/auth/socialauth')

    api.add_resource(SignupApi, '/auth/signup')
    api.add_resource(LoginApi, '/auth/login')
    api.add_resource(LogoutApi, '/auth/logout')

    api.add_resource(ForgotPassword, '/auth/forgot')
    api.add_resource(ResetPassword, '/auth/reset')

    api.add_resource(RenderHTMLApi, '/browser_client')
    api.add_resource(BusinessCardApi, '/<id>')
    api.add_resource(ShowCardApi, '/card/<id>')

