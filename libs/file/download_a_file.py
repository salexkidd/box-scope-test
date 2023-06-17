"""
Copy a file

- Create test file to target_user test folder by target_user
- The target user downscopes the client and downloads the created file.
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
        result["result"] = "Unknown(target_user can't create a file to target_user test folder."
        result["note"]["error"] = str(e)
        return result

    try:
        downscope_client = get_downscope_client(opt, user_client, target_user, target_user_created_file, scopes)
    except Exception as e:
        result["result"] = "NG"
        result["note"]["error"] = str(e)
        return result

    # The target user downscopes the client and downloads the created file.
    try:
        content = downscope_client.file(target_user_created_file.id).content()
        result["result"] = "SUCCESS"
        result["note"]["content"] = content.decode('utf-8')
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