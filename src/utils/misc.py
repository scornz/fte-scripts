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

    # If domain part is googlemail.com in any case, change it to gmail.com
    if domain_part.lower() == "googlemail.com" or domain_part.lower() == "gmail.com":
        # Change domain part to gmail.com
        domain_part = "gmail.com"
        # Remove all '.' characters from the local part
        local_part = local_part.replace(".", "")

    # Reconstruct and return the modified email
    return f"{local_part}@{domain_part}".lower().strip()
