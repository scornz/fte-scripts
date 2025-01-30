from pyairtable.orm import Model, fields as F

from utils.env import AIRTABLE_API_KEY, AIRTABLE_BASE_ID


class Division(Model):
    name = F.TextField("Name", readonly=True)
    num_athletes = F.IntegerField("# Athletes", readonly=True)

    class Meta:
        base_id = AIRTABLE_BASE_ID
        table_name = "Divisions"
        api_key = AIRTABLE_API_KEY
