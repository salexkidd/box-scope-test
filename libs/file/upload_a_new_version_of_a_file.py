"""
Upload a new version of a file

- Create test file to target_user test folder by target_user
- The target user downscopes the client and upgrades the created file.
"""
import sys

from boxsdk import Client
from boxsdk.object.user import User
from boxsdk.object.folder import Folder
from loguru import logger
import io
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


    # The target user downscopes the client and upgrades the created file.
    try:
        with io.StringIO("It's new version!") as fh:
            upload_new_version = downscope_client.file(target_user_created_file.id).update_contents_with_stream(fh)
        result["result"] = "SUCCESS"
        result["note"]["new_version"] = upload_new_version
    except Exception as e:
        result["result"] = "NG"
        result["note"]["error"] = str(e)
        return result

    assert target_user_created_file.file_version.id != upload_new_version.file_version.id

    # Destroy created file
    try:
        target_user_created_file.delete()
    except Exception as e:
        logger.warning(f"Can't delete temporary file for test. FILE_ID: {target_user_created_file.id}")

    return result
