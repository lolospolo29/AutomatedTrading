class MongoQueryBuilder:
    def __init__(self):
        self.query = {}
        self.projection = None
        self.sorting = []
        self.limit_value = None
        self.skip_value = None

    def filter(self, field: str, operator: str, value):
        operators = {
            "eq": "$eq",
            "gt": "$gt",
            "gte": "$gte",
            "lt": "$lt",
            "lte": "$lte",
            "ne": "$ne",
            "in": "$in",
            "nin": "$nin",
            "regex": "$regex"
        }

        if operator not in operators:
            raise ValueError(f"Invalid operator: {operator}")

        if field in self.query:
            self.query[field].update({operators[operator]: value})
        else:
            self.query[field] = {operators[operator]: value}

        return self

    def and_filter(self, *conditions):
        if "$and" not in self.query:
            self.query["$and"] = []
        self.query["$and"].extend(conditions)
        return self

    def select(self, *fields):
        self.projection = {field: 1 for field in fields}
        return self

    def sort(self, field: str, direction: str = "asc"):
        order = 1 if direction == "asc" else -1
        self.sorting.append((field, order))
        return self

    def limit(self, value: int):
        self.limit_value = value
        return self

    def skip(self, value: int):
        self.skip_value = value
        return self

    def build(self):
        query_object = {"filter": self.query}
        if self.projection:
            query_object["projection"] = self.projection
        if self.sorting:
            query_object["sort"] = self.sorting
        if self.limit_value is not None:
            query_object["limit"] = self.limit_value
        if self.skip_value is not None:
            query_object["skip"] = self.skip_value
        return query_object


# Example Usage
query_builder = (MongoQueryBuilder()
                 .and_filter({"brand": {"$eq": "Apple"}}, {"stock": {"$gt": 0}})
                 )

query = query_builder.build()
print(query)
