"""
Find a file for a shared link
- Create test file to target_user test folder by target_user and create shared link
- Find shared links in downscoped clients
"""
import sys

from boxsdk import Client
from boxsdk.object.collaboration import CollaborationRole
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
    shared_link = None

    result = {
        "result": "NG",
        "note": {},
    }

    # Create test file to target_user test folder by target_user
    try:
        target_user_created_file = creates_file_at_the_specified_client(user_client, test_folder.id)
        shared_link = target_user_created_file.create_shared_link(access="open").shared_link["url"]
    except Exception as e:
        result["result"] = "Unknown(target_user can't create a file to target_user root folder."
        result["note"]["error"] = str(e)
        return result

    assert target_user_created_file is not None
    assert shared_link is not None

    try:
        downscope_client = get_downscope_client(opt, user_client, target_user, target_user_created_file, scopes)
    except Exception as e:
        result["result"] = "NG"
        result["note"]["error"] = str(e)
        return result

    # Find shared links in downscoped clients
    try:
        finded_file = downscope_client.get_shared_item(shared_link)
        result["result"] = "SUCCESS"
        result["note"]["file"] = finded_file.response_object
    except Exception as e:
        result["result"] = "NG"
        result["note"]["error"] = str(e)
        return result

    # Destroy created file
    try:
        target_user_created_file.delete()
    except Exception as e:
        logger.warning(f"Can't delete temporary file for test. FILE_ID: {target_user_created_file.id}")

    return result