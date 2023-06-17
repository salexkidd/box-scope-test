from boxsdk import Client, JWTAuth, OAuth2
import uuid
import logging
import sys

logging.getLogger('boxsdk').setLevel(logging.CRITICAL)

TARGET_USER = "11458579583"
TARGET_FILE = "1237463715284"
TARGET_FOLDER = "212366513969"


class Fuck(Exception):
    ...


def get_auth(user=None):
    return JWTAuth.from_settings_file(
        "/Users/traincrash/Downloads/JWTAccessTest.json", user=user)

def get_user_auth(access_token):
    return OAuth2(
        client_id=None,
        client_secret=None,
        access_token=access_token
    )


def get_downscope_access_token(client, item, scopes):
    return client.downscope_token(scopes, item).access_token


def get_client(auth):
    return Client(auth)


def main():
    sa_client = Client(get_auth())

    target_user = sa_client.user(TARGET_USER).get()
    target_file = sa_client.file(TARGET_FILE).get()
    target_folder = sa_client.folder(TARGET_FOLDER).get()

    user_auth = get_auth(user=target_user)

    user_client = get_client(user_auth)
    downscope_file_client = get_client(get_user_auth(get_downscope_access_token(user_client, target_file, ["item_read"])))
    downscope_folder_client = get_client(get_user_auth(get_downscope_access_token(user_client, target_folder, ["item_read"])))

    # Normal User
    user_client.file(TARGET_FILE).content()
    [item for item in user_client.folder(TARGET_FOLDER).get_items()]

    assert user_client.folder(TARGET_FOLDER).get().shared_link != None

    # ---------------------------------------------------------------------------------------------------------

    # Downscope from file
    downscope_file_client.file(TARGET_FILE).content()
    try:
        [item for item in downscope_file_client.folder(TARGET_FOLDER).get_items()]
        raise Fuck()
    except Fuck:
        print("Fuck!")
        sys.exit(1)
    except Exception as e:
        ...

    try:
        downscope_file_client.folder(TARGET_FOLDER).get().shared_link
        raise Fuck()
    except Fuck:
        print("Fuck!")
        sys.exit(1)
    except Exception as e:
        ...

    # ---------------------------------------------------------------------------------------------------------

    # Downscope from folder
    try:
        downscope_folder_client.file(TARGET_FILE).content()
    except Exception as e:
        ...

    [item for item in downscope_folder_client.folder(TARGET_FOLDER).get_items()]
    assert downscope_folder_client.folder(TARGET_FOLDER).get().shared_link == None



main()

