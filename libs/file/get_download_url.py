"""
Get download url

- Create test file to target_user test folder by target_user
- The target user downscopes the client and get download url.
"""
import sys

from boxsdk import Client
from boxsdk.object.user import User
from boxsdk.object.folder import Folder
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
    target_uesr_created_file = None

    result = {
        "result": "NG",
        "note": {},
    }

    # Create test file to target_user test folder by target_user
    try:
        target_uesr_created_file = creates_file_at_the_specified_client(user_client, test_folder.id)
    except Exception as e:
        result["result_text"] = "Unknown(target_user can't create a file to target_user root folder."
        result["result"] = False
        result["error"] = str(e)
        return result

    try:
        downscope_client = get_downscope_client(opt, user_client, target_user, target_uesr_created_file, scopes)
    except Exception as e:
        result["result_text"] = "NG"
        result["result"] = False
        result["error"] = str(e)
        return result

    # The target user downscopes the client and get download url.
    try:
        url = downscope_client.file(target_uesr_created_file.id).get_download_url()
        result["result_text"] = "SUCCESS"
        result["result"] = True
        result["note"]["download_url"] = url
    except Exception as e:
        result["result_text"] = "NG"
        result["result"] = False
        result["error"] = str(e)
        return result

    # Destroy created file
    try:
        target_uesr_created_file.delete()
    except Exception as e:
        logger.warning(f"Can't delete temporary file for test. FILE_ID: {f.id}")

    return result
