import numbers
import numbers
from pydantic import Field
from pydantic import BaseModel

class AirBnbSchema(BaseModel): 
     _id: str = Field(alias="_id")
     name: str
     summary: str
     description: str
     notes: str
     home_rules: str
     property_type: str
     room_type: str
     minimum_nights: str
     maximum_nights: str
     price: numbers
     weekly_price: numbers
     monthly_price: numbers
     cleaning_fee: numbers
     

