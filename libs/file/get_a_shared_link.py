"""
create or update a shared link
- Create test file to target_user test folder by target_user
- Create a shared link on the client where the target user.
- Target user downscoped client to get shared link.

"""
import sys

from boxsdk.object.collaboration import CollaborationRole
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
def test_func(opt, sa_client, user_client, target_user, test_folder, scopes):
    target_user_created_file = None

    result = {
        "result": "NG",
        "note": {},
    }

    # Create test file to target_user test folder by target_user
    try:
        target_user_created_file = creates_file_at_the_specified_client(user_client, test_folder.id)
    except Exception as e:
        result["result"] = "Unknown(target_user can't create a file to target_user test folder."
        result["note"]["error"] = str(e)
        return result

    try:
        downscope_client = get_downscope_client(opt, user_client, target_user, target_user_created_file, scopes)
    except Exception as e:
        result["result"] = "NG"
        result["note"]["error"] = str(e)
        return result


    # Create a shared link on the client where the target user.
    try:
        target_user_created_file.get_shared_link(access="open")
    except Exception as e:
        result["result"] = "NG"
        result["note"]["error"] = str(e)
        return result

    # Target user downscoped client to get shared link.
    try:
        url = downscope_client.file(target_user_created_file.id).get().shared_link
        result["result"] = "SUCCESS"
        result["note"]["shared_link"] = url
    except Exception as e:
        result["result"] = "NG"
        result["note"]["error"] = str(e)


    # Destroy created file
    try:
        target_user_created_file.delete()
    except Exception as e:
        logger.warning(f"Can't delete temporary file for test. FILE_ID: {target_user_created_file.id}")

    return result