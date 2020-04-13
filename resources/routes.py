from .movie import MoviesApi, MovieApi
from .event_detail import EventDetailsApi, EventDetailApi
from .image_detail import DisplayImageApi, UploadImageApi
from .auth import SignupApi, LoginApi, LogoutApi
from .reset_password import ForgotPassword, ResetPassword


def initialize_routes(api):
    api.add_resource(MoviesApi, '/movies')
    api.add_resource(MovieApi, '/movies/<id>')

    api.add_resource(EventDetailsApi, '/event_details')
    api.add_resource(EventDetailApi, '/event_details/<id>')

    api.add_resource(UploadImageApi, '/upload_image')
    api.add_resource(DisplayImageApi, '/display_image/<id>')

    api.add_resource(SignupApi, '/auth/signup')
    api.add_resource(LoginApi, '/auth/login')
    api.add_resource(LogoutApi, '/logout')

    api.add_resource(ForgotPassword, '/auth/forgot')
    api.add_resource(ResetPassword, '/auth/reset')
