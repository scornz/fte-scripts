def process_email(email: str):
    """
    Returns the email address with all '.' characters removed
    from the portion before the '@' symbol.

    Arguments:
        email (`str`): The email address to process.

    Returns:
        out (`str`): The modified email address.

    """

    # Split into local part (before '@') and domain part (after '@')
    local_part, domain_part = email.split("@", 1)

    # Remove all '.' characters from the local part
    local_part_without_periods = local_part.replace(".", "")

    # If domain part is googlemail.com in any case, change it to gmail.com
    if domain_part.lower() == "googlemail.com":
        domain_part = "gmail.com"

    # Reconstruct and return the modified email
    return f"{local_part_without_periods}@{domain_part}".lower().strip()
