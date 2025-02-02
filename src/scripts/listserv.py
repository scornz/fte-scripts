from utils.db import Group
from utils.log import logger
from utils.google import (
    google_add_user_to_group,
    google_create_group,
    google_fetch_all_groups,
    google_get_all_group_members,
    google_remove_user_from_group,
    google_update_group_managers,
)

from time import sleep

from utils.misc import process_email


def main():
    """Fetches all groups from the database, and then creates new groups in
    Google Workspace if necessary. If a group already exists in Google Workspace,
    do nothing. Users will be added/removed from the groups accordingly.
    """

    # STEP 1: Dynamically create groups in Google Workspace based on the groups in the database
    logger.info(
        "1: Dynamically creating groups in Google Workspace based on the groups in the database."
    )
    groups = Group.all()
    google_groups = {g["email"]: g for g in google_fetch_all_groups()}
    for group in groups:
        email = group.email
        if email in google_groups:
            logger.info(f"Group {email} already exists in Google Workspace.")
            continue

        google_groups[email] = google_create_group(email, group.name, group.description)

    # STEP 2: Add/remove users from the groups in Google Workspace
    logger.info("2: Adding/removing users from the groups in Google Workspace.")
    for group in groups:
        members = set([process_email(m.email) for m in group.athletes])
        google_group_members = google_get_all_group_members(group.email)
        logger.info(f"Fetched {len(google_group_members)} members of {group.email}.")

        # Add users who are supposed to be in the group
        for member in members:
            if member not in google_group_members:
                google_add_user_to_group(member, group.email)

        # Remove users who are not supposed to be in the group
        for member in google_group_members:
            if member not in members:
                google_remove_user_from_group(member, group.email)

    # STEP 3: Update the managers of the groups in Google Workspace
    logger.info("3: Updating the managers of the groups in Google Workspace.")
    for group in groups:
        managers = [m.email for m in group.managers]
        google_update_group_managers(group.email, managers)


if __name__ == "__main__":
    main()
