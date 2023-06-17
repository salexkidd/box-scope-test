"""
Get a files information

- Create test file to target_user test folder by target_user
- Retrieve information on files collaborated by the target user.
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

# https://ja.developer.box.com/reference/resources/file--full/#param-expiring_embed_link
ALL_FILE_FIELDS = [
    "id", "type", "allowed_invitee_roles", "classification", "comment_count", "content_created_at", "created_at",
    "created_by", "description", "disposition_at", "etag", "expires_at", "extension",
    # "expiring_embed_link", <- Unsupported Media Type... WTF!?
    "file_version", "has_collaborations", "is_accessible_via_shared_link", "is_externally_owned", "is_package",
    "item_status", "lock", "metadata", "modified_at", "modified_by", "name", "owned_by", "parent", "path_collection",
    "permission", "purged_at", "representations", "sequence_id", "sha1", "shared_link", "shared_link_permission_options",
    "size", "targs", "trashed_at", "uploader_display_name", "version_number", "watermark_info",
]


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

    # Get downscope client
    try:
        downscope_client = get_downscope_client(opt, user_client, target_user, target_user_created_file, scopes)
    except Exception as e:
        result["result"] = "NG"
        result["note"]["error"] = str(e)
        return result

    # Retrieve information on files collaborated by the target user.
    try:
        file_info = downscope_client.file(target_user_created_file.id).get(fields=ALL_FILE_FIELDS)
        result["result"] = "SUCCESS"
        result["note"]["information"] = file_info.response_object
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