import json
import datetime
from json import JSONEncoder

class DateTimeEncoder(JSONEncoder):
        #Override the default method
        def default(self, obj):
            if isinstance(obj, (datetime.date, datetime.datetime)):
                return obj.isoformat()


# custom Decoder
# def DecodeDateTime(datestr):
#     newdate = datetime.fromisoformat(datestr)
#     return newdate



# decodedJSON = json.loads(jsonData, object_hook=DecodeDateTime)
# print(DateTimeEncoder().encode(employee))
# print("Encode DateTime Object into JSON using custom JSONEncoder")
# employeeJSONData = json.dumps(employee, indent=4, cls=DateTimeEncoder)