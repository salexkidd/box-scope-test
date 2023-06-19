"""
Get a previous version os a file

- Create test file to target_user test folder by target_user and update 2times
- Retrieve past versions with downscoped clients.
"""
import sys
import io
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

    # Create test file to target_user test folder by target_user and update
    try:
        target_user_created_file = creates_file_at_the_specified_client(user_client, test_folder.id)
        for i in range(2):
            with io.StringIO("It's new version 1!") as fh:
                upload_new_version = user_client.file(target_user_created_file.id).update_contents_with_stream(fh)


    except Exception as e:
        result["result_text"] = "Unknown(target_user can't create a file to target_user root folder."
        result["result"] = False
        result["error"] = str(e)
        return result

    try:
        downscope_client = get_downscope_client(opt, user_client, target_user, target_user_created_file, scopes)
    except Exception as e:
        result["result_text"] = "NG"
        result["result"] = False
        result["error"] = str(e)
        return result

    # Retrieve past versions with downscoped clients.
    try:
        versions = downscope_client.file(target_user_created_file.id).get_previous_versions()
        result["result_text"] = "SUCCESS"
        result["result"] = True
        result["note"]["previous_version"] = [v.response_object for v in versions]
    except Exception as e:
        result["result_text"] = "NG"
        result["result"] = False
        result["error"] = str(e)
        return result

    assert target_user_created_file.file_version.id != upload_new_version.file_version.id

    # Destroy created file
    try:
        target_user_created_file.delete()
    except Exception as e:
        logger.warning(f"Can't delete temporary file for test. FILE_ID: {target_user_created_file.id}")

    return result
