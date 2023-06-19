"""
Lock a file

- Create test file to target_user test folder by target_user
- The created file is locked by target_user.
- Unlock the locked file with the downscoped client.
"""
import io
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
        result["result_text"] = "Unknown(target_user can't create a file to target_user test folder."
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

    # The created file is locked by target_user.
    try:
        moved_file = target_user_created_file.lock()
    except Exception as e:
        result["result_text"] = "NG"
        result["result"] = False
        result["error"] = str(e)
        return result

    # Unlock the locked file with the downscoped client.
    try:
        moved_file = downscope_client.file(target_user_created_file.id).unlock()
        result["result_text"] = "SUCCESS"
        result["result"] = True
        result["note"]["file"] = moved_file
    except Exception as e:
        result["result_text"] = "NG"
        result["error"] = str(e)
        return result

    # Destroy created file
    try:
        moved_file.delete()
    except Exception as e:
        logger.warning(f"Can't delete temporary file for test. FILE_ID: {moved_file.id}")

    return result