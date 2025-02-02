from pyairtable.orm import Model, fields as F

from utils.db.athlete import Athlete
from utils.env import AIRTABLE_API_KEY, AIRTABLE_BASE_ID


class Group(Model):
    name = F.TextField("Name")
    email = F.TextField("Email")
    description = F.TextField("Description")
    athletes = F.LinkField[Athlete]("Athletes", Athlete)
    managers = F.LinkField[Athlete]("Managers", Athlete)

    class Meta:
        base_id = AIRTABLE_BASE_ID
        table_name = "Groups"
        api_key = AIRTABLE_API_KEY
