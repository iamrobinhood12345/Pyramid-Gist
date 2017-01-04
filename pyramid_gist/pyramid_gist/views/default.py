from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from pyramid_gist.models import MyModel

from pyramid.view import view_config, forbidden_view_config
from pyramid.httpexceptions import HTTPFound
import datetime
from pyramid_gist.security import check_credentials
from pyramid.security import remember, forget  # <--- add this line


@view_config(route_name='home', renderer='../templates/home.jinja2')
def home_view(request):
    try:
        query = request.dbsession.query(MyModel)
        one = query.all()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'project': 'pyramid_gist'}


@view_config(route_name="login",
             renderer="../templates/login.jinja2",
             require_csrf=False)
def login_view(request):
    """Authenticate the incoming user."""
    if request.POST:
        username = request.POST["username"]
        password = request.POST["password"]
        if check_credentials(username, password):
            auth_head = remember(request, username)
            return HTTPFound(
                request.route_url("home"),
                headers=auth_head
            )

    return {}


@view_config(route_name="logout")
def logout_view(request):
    """Remove authentication from the user."""
    auth_head = forget(request)
    return HTTPFound(request.route_url("home"), headers=auth_head)


@view_config(route_name="register",
             renderer="../templates/register.jinja2",
             require_csrf=False)
def register_view(request):
    """Authenticate the incoming user."""
    if request.method == "POST":
        new_username = request.POST["username"]
        new_password = request.POST["password"]
        new_email = request.POST["email"]
        new_first_name = request.POST["first_name"]
        new_last_name = request.POST["last_name"]
        new_favorite_food = request.POST["favorite_food"]

        model = MyModel(username=new_username, password=new_password, email=new_email, first_name=new_first_name, last_name=new_last_name, favorite_food=new_favorite_food)
        request.dbsession.add(model)

        # request.dbsession.flush()
        return HTTPFound(request.route_url("profile/" + new_username))

    return {}


@view_config(route_name='profile', renderer='../templates/profile.jinja2', permission='secret')
def profile_view(request):
    usernamed = request.matchdict['username']
    try:
        entry = request.dbsession.query(MyModel).get(usernamed)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'ENTRIES': entry, 'project': 'pyramid_gist'}


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_pyramid_gist_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
