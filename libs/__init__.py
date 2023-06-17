import glob
import io
import types
import uuid
from importlib import import_module

from boxsdk import Client, JWTAuth, OAuth2
from boxsdk.object.item import Item
from boxsdk.object.user import User
from loguru import logger


def load_test_modules(opt):
    modules = list()

    use_modules = None
    if opt["--tests"]:
        use_modules = opt["--tests"].split(",")

    for name in glob.glob(f"libs/**/*.py", recursive=True):
        name = name.replace("/", ".").replace(".py", "")
        if name.split(".")[-1] == "__init__":
            continue

        try:
            module = import_module(name)
        except Exception as e:
            logger.error(f"can't load {name}. error:{e}")
            continue

        if module.USE:
            if use_modules:
                if module.__name__ in use_modules:
                    modules.append(module)
            else:
                modules.append(module)

    return modules


def get_auth(opt, user:User=None) -> JWTAuth:
    return JWTAuth.from_settings_file(opt["<JWT-FILE>"], user=user)


def get_user_auth(access_token: str) -> OAuth2:
    return OAuth2(
        client_id=None,
        client_secret=None,
        access_token=access_token
    )


def get_downscope_access_token(client:Client, item:Item, scopes: list) -> str:
    return client.downscope_token(scopes, item).access_token


def get_downscope_client(opt, client:Client, user:User, item, scopes:list) -> Client:
    if scopes:
        return get_client(get_user_auth(get_downscope_access_token(client, item, scopes)))
    else:
        return get_client(get_user_auth(get_auth(opt, user=user).authenticate_user()))


def get_client(auth) -> Client:
    return Client(auth)


def get_target_user(client:Client, target_user_id: int) -> User:
    return client.user(target_user_id).get()


def creates_file_at_the_specified_client(client: Client, folder_id:int=0) -> io.TextIOWrapper:
    folder = client.folder(folder_id)
    with io.StringIO("THIS IS TEST FILE") as fs:
        return folder.upload_stream(fs, f"Scope-Test-file-{uuid.uuid4().hex}")


def report(func:types.FunctionType):
    def _wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            logger.debug(f"{func.__module__}: {result}")
            return result
        except Exception as error:
            logger.error(error)
            return {"result": "NG", "note": {"error": str(error)}}

    return _wrapper
