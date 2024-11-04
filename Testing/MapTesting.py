class Mapper:
    def MapToClass(self, data):
        # Check if '_id' exists in data and extract it as `object_id`
        object_id = data.get("_id", None)

        # Remove '_id' from data if it exists so that the rest of the fields can be mapped
        if "_id" in data:
            del data["_id"]

        # Map remaining data fields to class properties or return a dictionary with `_id` and other data
        mapped_object = {
            "ObjectId": str(object_id),  # Optional: convert `_id` to a string for easier handling
            "Data": data
        }

        return mapped_object

# Usage example
mapper = Mapper()
mongo_data = {"_id": "670544f05e70a5a24322cce4", "name": "Trade", "type": "Object"}
mapped_result = mapper.MapToClass(mongo_data)
print(mapped_result)