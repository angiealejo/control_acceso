from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse, RegexURLPattern, RegexURLResolver
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.functional import lazy
from django.utils.http import urlquote

from functools import wraps

from apps.comun.views import http401
# Funciones para que una url solo sea accesada segun se requiera

no_logeado = user_passes_test(lambda u: u.is_anonymous(), lazy(reverse, str)('home'))


def user_passes_test_with_403(test_func, login_url=None):
    """
    View decorator that checks to see if the user passes the specified test.
    See :meth:`django.contrib.auth.decorators.user_passes_test`.

    Anonymous users will be redirected to login_url, while logged in users that
    fail the test will be given a 403 error.  In the case of a 403, the function
    will render the **403.html** template.
    """
    if not login_url:
        from django.conf import settings
        login_url = settings.LOGIN_URL

    def _dec(view_func):
        @wraps(view_func)
        def _checklogin(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            elif not request.user.is_authenticated():
                return HttpResponseRedirect('%s?%s=%s' % (login_url,
                                                          REDIRECT_FIELD_NAME, urlquote(request.get_full_path())))
            else:
                raise PermissionDenied
        return _checklogin
    return _dec


def permission_required_with_403(perm, login_url=None):
    """
    Decorator for views that checks whether a user has a particular permission
    enabled, redirecting to the login page or rendering a 403 as necessary.

    See :meth:`django.contrib.auth.decorators.permission_required`.
    """
    return user_passes_test_with_403(lambda u: u.has_perm(perm), login_url=login_url)

# ajax permissions decorators adapted from
# http://drpinkpony.wordpress.com/2010/02/02/django-ajax-authentication/


def user_passes_test_with_ajax(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.

    Returns special response to ajax calls instead of blindly redirecting.

    To use with class methods instead of functions, use :meth:`django.utils.decorators.method_decorator`.  See
    http://docs.djangoproject.com/en/dev/releases/1.2/#user-passes-test-login-required-and-permission-required
    """
    if not login_url:
        from django.conf import settings
        login_url = settings.LOGIN_URL

    def decorator(view_func):
        @wraps(view_func)
        def _check_user_test(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            path = urlquote(request.get_full_path())
            urlparts = login_url, redirect_field_name, path
            # check for ajax request
            if not request.is_ajax():
                return HttpResponseRedirect('%s?%s=%s' % urlparts)
            else:
                # In case of ajax we send 401 - unauthorized HTTP response
                return HttpResponse('%s?%s=%s' % urlparts, status=401)

        return _check_user_test
    return decorator


def login_required_with_ajax(function=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary, but returns a special response for ajax requests.
    See :meth:`eulcore.django.auth.decorators.user_passes_test_with_ajax`.
    """
    if function is None:
        function = lambda u: u.is_authenticated()
    return user_passes_test_with_ajax(function, redirect_field_name=redirect_field_name)


def permission_required_with_ajax(perm, login_url=None):
    """
    Decorator for views that checks whether a user has a particular permission
    enabled, redirecting to the log-in page if necessary, but returns a special
    response for ajax requests.  See :meth:`eulcore.django.auth.decorators.user_passes_test_with_ajax`.
    """
    return user_passes_test_with_ajax(lambda u: u.has_perm(perm), login_url=login_url)


def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated():
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test_with_403(in_groups)


def not_group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated():
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return False
        return True
    return user_passes_test_with_403(in_groups)


class DecoratedURLPattern(RegexURLPattern):
    def resolve(self, *args, **kwargs):
        result = super(DecoratedURLPattern, self).resolve(*args, **kwargs)
        if result:
            result.func = self._decorate_with(result.func)
        return result


class DecoratedRegexURLResolver(RegexURLResolver):
    def resolve(self, *args, **kwargs):
        result = super(DecoratedRegexURLResolver, self).resolve(*args, **kwargs)
        if result:
            result.func = self._decorate_with(result.func)
        return result


def decorated_includes(func, includes, *args, **kwargs):
    urlconf_module, app_name, namespace = includes

    for item in urlconf_module:
        if isinstance(item, RegexURLPattern):
            item.__class__ = DecoratedURLPattern
            item._decorate_with = func

        elif isinstance(item, RegexURLResolver):
            item.__class__ = DecoratedRegexURLResolver
            item._decorate_with = func

    return urlconf_module, app_name, namespace


def staff_super_usuario_logeado():
    """Requires user membership in at least one of the groups passed in."""
    def sus(u):
        if u.is_authenticated() and u.is_active and u.is_staff and u.is_superuser:
            return True
        else:
            return False
    return user_passes_test_with_401(sus)


def user_passes_test_with_401(test_func, login_url=None):
    """
    View decorator that checks to see if the user passes the specified test.
    See :meth:`django.contrib.auth.decorators.user_passes_test`.

    Anonymous users will be redirected to login_url, while logged in users that
    fail the test will be given a 403 error.  In the case of a 403, the function
    will render the **403.html** template.
    """
    if not login_url:
        from django.conf import settings
        login_url = settings.LOGIN_URL

    def _dec(view_func):
        @wraps(view_func)
        def _checklogin(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            elif not request.user.is_authenticated():
                return HttpResponseRedirect('%s?%s=%s' % (login_url,
                                                          REDIRECT_FIELD_NAME, urlquote(request.get_full_path())))
            else:
                return http401(request)
        return _checklogin
    return _dec
