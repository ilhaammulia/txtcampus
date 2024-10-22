import base64
from flask import g, request
from src.services.session_service import SessionService
from src.error import UnauthorizedError, InternalServerError, NotFoundError, BadRequestError, ForbiddenError

def auth_required(f):
    def decorator(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token:
            try:
                session = SessionService.get_session(token)
                if not session:
                    raise UnauthorizedError("Unauthorized.")
                g.current_user = session.user
                return f(*args, **kwargs)
            except NotFoundError as err:
                raise NotFoundError(err.message)
            except BadRequestError as err:
                raise BadRequestError(err.message)
            except ForbiddenError as err:
                raise ForbiddenError(err.message)
            except UnauthorizedError as err:
                raise UnauthorizedError(err.message)
            except Exception as err:
                print(err)
                raise InternalServerError("Server Error")
        raise UnauthorizedError("Authorization token is missing")
    return decorator
