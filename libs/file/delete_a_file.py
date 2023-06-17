"""
Delete a file

- Create test file to target_user test folder by target_user
- Deletes files created by the target user on the downscoped client.
"""
import io
import sys

from boxsdk import Client
from boxsdk.object.folder import Folder
from boxsdk.object.user import User
from loguru import logger

sys.path.append("../../")
from libs import (creates_file_at_the_specified_client, get_downscope_client,
                  report)

__all__ = (
    "USE",
    "test_func",
)

USE = True


@report
def test_func(opt, sa_client:Client, user_client:Client, target_user:User, test_folder:Folder, scopes: list):
    target_user_created_file = None

    result = {
        "result": "NG",
        "note": {},
    }

    # Create test file to target_user test folder by target_user
    try:
        target_user_created_file = creates_file_at_the_specified_client(user_client, test_folder.id)
    except Exception as e:
        result["result"] = "Unknown(target_user can't create a file to target_user root folder."
        result["note"]["error"] = str(e)
        return result

    try:
        downscope_client = get_downscope_client(opt, user_client, target_user, target_user_created_file, scopes)
    except Exception as e:
        result["result"] = "NG"
        result["note"]["error"] = str(e)
        return result

    # Deletes files created by the target user on the downscoped client.
    try:
        downscope_client.file(target_user_created_file.id).delete()
        result["result"] = "SUCCESS"

    except Exception as e:
        result["result"] = "NG!"
        result["note"]["error"] = str(e)

    return result