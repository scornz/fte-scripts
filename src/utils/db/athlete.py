from pyairtable.orm import Model, fields as F

from .division import Division
from utils.env import AIRTABLE_API_KEY, AIRTABLE_BASE_ID


class Athlete(Model):
    full_name = F.TextField("Full Name", readonly=True)
    first_name = F.TextField("First Name")
    last_name = F.TextField("Last Name")

    headshot = F.AttachmentsField("Headshot")

    status = F.SelectField("Status")
    source = F.SelectField("Source")
    payment_type = F.SelectField("Payment Type")
    email = F.TextField("Email")

    phone = F.PhoneNumberField("Phone")
    dob = F.DateField("DOB")
    instagram = F.TextField("Instagram")

    ag_division = F.SingleLinkField[Division]("AG Division", Division)

    garmin_profile = F.TextField("Garmin Profile")
    strava_profile = F.TextField("Strava Profile")
    training_peaks_account = F.TextField("Training Peaks Account")
    zwift_account = F.TextField("Zwift Account")
    race_kit_size = F.TextField("Race Kit Size")
    shirt = F.TextField("Shirt")
    shoe = F.TextField("Shoe")
    pant = F.TextField("Pant")

    created = F.CreatedTimeField("Created")

    class Meta:
        base_id = AIRTABLE_BASE_ID
        table_name = "Athletes"
        api_key = AIRTABLE_API_KEY
