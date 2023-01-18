from flask import Flask, jsonify, Response
from authlib.integrations.flask_oauth2 import ResourceProtector
from validator import ZitadelIntrospectTokenValidator, ValidatorError

require_auth = ResourceProtector()
require_auth.register_token_validator(ZitadelIntrospectTokenValidator())

APP = Flask(__name__)

@APP.errorhandler(ValidatorError)
def handle_auth_error(ex: ValidatorError) -> Response:

    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

@APP.route("/api/public")
def public():
    """No access token required."""
    response = (
        "Public route - You don't need to be authenticated to see this."
    )
    return jsonify(message=response)


@APP.route("/api/private")
@require_auth(None)
def private():
    """A valid access token is required."""
    response = (
        "Private route - You need to be authenticated to see this."
    )
    return jsonify(message=response)


@APP.route("/api/private-scoped")
@require_auth(["read:messages"])
def private_scoped():
    """A valid access token and scope are required."""
    response = (
        "Private, scoped route - You need to be authenticated and have the role read:messages to see this."
    )
    return jsonify(message=response)

if __name__ == "__main__":
    APP.run()