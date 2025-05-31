from src.controllers.utils import requires_role
import pytest
from http import HTTPStatus


def test_requires_role(mocker):
    #Given (o que eu forneço para o teste)
    user_mock = mocker.Mock()
    user_mock.role.name = "admin"

    mocker.patch('src.controllers.utils.get_jwt_identity')
    mocker.patch('src.controllers.utils.db.get_or_404', return_value=user_mock)
    decorated_function = requires_role("admin")(lambda: "Success")

    #When (o que eu executo)
    result = decorated_function()
    
    #Then (o que eu verifico)
    assert result == "Success"
    
    
def test_requires_role_fail(mocker):
    #Given (o que eu forneço para o teste)
    user_mock = mocker.Mock()
    user_mock.role.name = "normal"

    mocker.patch('src.controllers.utils.get_jwt_identity')
    mocker.patch('src.controllers.utils.db.get_or_404', return_value=user_mock)
    decorated_function = requires_role("admin")(lambda: "Success")

    #When (o que eu executo)
    result = decorated_function()
    
    #Then (o que eu verifico)
    assert result == ({"message": "User dont have access for this operation."}, HTTPStatus.FORBIDDEN)

