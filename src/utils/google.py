from __future__ import annotations
from time import sleep

from utils.env import GOOGLE_SERVICE_ACCOUNT_CREDENTIALS
from utils.log import logger
from google.oauth2 import service_account
from googleapiclient.discovery import build
import logging

from typing import List, TYPE_CHECKING

from utils.misc import process_email

if TYPE_CHECKING:
    from googleapiclient._apis.admin.directory_v1 import Group  # type: ignore


_google_service_creds = service_account.Credentials.from_service_account_info(
    GOOGLE_SERVICE_ACCOUNT_CREDENTIALS
)

dirv1 = build("admin", "directory_v1", credentials=_google_service_creds)


def google_fetch_all_groups(domain: str = "fullthrottle.nyc") -> List[Group]:
    """Fetch all groups that exist within a domain in Google Workspace.

    Arguments:
        domain (`str`, optional): The domain to search for groups. Defaults to "fullthrottle.nyc".

    Returns:
        out (`List[Group]`): A list of groups that exist within the domain.
    """

    res = dirv1.groups().list(domain=domain).execute()
    if "groups" in res:
        return res["groups"]

    return []


def google_create_group(email: str, name: str, description: str) -> Group:
    """Create a new group in Google Workspace.

    Arguments:
        email (`str`): The email address of the group.
        name (`str`): The name of the group.
        description (`str`): The description of the group.

    Returns:
        out (`Group`): The newly created group.
    """

    # Check if the group exists first by fetching it using the email address, do NOT use google_fetch_all_groups
    try:
        return dirv1.groups().get(groupKey=email).execute()
    except Exception:
        pass

    logging.info(f"Creating Google Group with email ({email}) and name ({name}).")
    body: Group = {"email": email, "name": name, "description": description}

    group = dirv1.groups().insert(body=body).execute()
    logger.info(f"Waiting for 60s after creating group {email}.")
    sleep(60)
    return group


def google_get_all_group_members(group_email: str) -> List[str]:
    """Get all members of a group in Google Workspace.

    Arguments:
        group_email (`str`): The email address of the group.

    Returns:
        out (`List[str]`): A list of email addresses of the members.
    """

    all_members = []
    page_token = None

    while True:
        if page_token:
            res = (
                dirv1.members()
                .list(groupKey=group_email, pageToken=page_token, maxResults=200)
                .execute()
            )
        else:
            res = dirv1.members().list(groupKey=group_email, maxResults=200).execute()

        if "members" in res:
            all_members.extend([process_email(m["email"]) for m in res["members"]])

        # Check if there are more pages
        page_token = res.get("nextPageToken")
        if not page_token:
            break

    return all_members


def google_add_user_to_group(email: str, group_email: str):
    """Add a user to a group in Google Workspace.

    Arguments:
        email (`str`): The email address of the user.
        group_email (`str`): The email address of the group.
    """

    email = process_email(email)
    logger.info(f"Adding {email} to {group_email}.")
    try:
        dirv1.members().insert(groupKey=group_email, body={"email": email}).execute()
    except Exception as e:
        logger.error(f"Failed to add {email} to {group_email}: {e}")

    sleep(1)


def google_remove_user_from_group(email: str, group_email: str):
    """Remove a user from a group in Google Workspace.

    Arguments:
        email (`str`): The email address of the user.
        group_email (`str`): The email address of the group.
    """

    email = process_email(email)
    logger.info(f"Removing {email} from {group_email}.")

    try:
        dirv1.members().delete(groupKey=group_email, memberKey=email).execute()
    except Exception as e:
        logger.error(f"Failed to remove {email} from {group_email}: {e}")

    sleep(1)


def google_update_group_managers(group_email: str, managers: List[str]):
    """Update the managers of a group in Google Workspace.

    Arguments:
        group_email (`str`): The email address of the group.
        managers (`List[str]`): The email addresses of the managers.
    """

    managers = [process_email(m) for m in managers]
    all_members = (
        dirv1.members().list(groupKey=group_email).execute().get("members", [])
    )

    # List of IDs to demote to members
    remove_manager_member_ids = [
        m["id"]
        for m in all_members
        if m["role"] == "MANAGER" and process_email(m["email"]) not in managers
    ]

    # List of IDs to promote to managers
    manager_member_ids = [
        m["id"]
        for m in all_members
        if process_email(m["email"]) in managers and m["role"] == "MEMBER"
    ]

    # Update the group's managers
    for member_id in manager_member_ids:
        logger.info(f"Promoting {member_id} to manager in {group_email}.")
        dirv1.members().update(
            groupKey=group_email, memberKey=member_id, body={"role": "MANAGER"}
        ).execute()
        sleep(1)

    # Demote the managers to members
    for member_id in remove_manager_member_ids:
        logger.info(f"Demoting {member_id} to member in {group_email}.")
        dirv1.members().update(
            groupKey=group_email, memberKey=member_id, body={"role": "MEMBER"}
        ).execute()
        sleep(1)
