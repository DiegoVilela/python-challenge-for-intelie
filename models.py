class Entity:
    """Represents an entity that can have many facts"""

    def __init__(self, name: str, facts: list, schema: list):
        self.name = name
        self.facts = facts
        self.schema = schema

    @property
    def fresh_facts(self):
        fresh = []
        for a in self.get_distinct_attributes():
            attr_cardinality = self.cardinality(a)
            fresh.extend(self.get_facts_by_attribute(a, attr_cardinality))
        return fresh

    def get_last_fact(self, attribute: str):
        """Returns the last fact of a given attribute"""
        return self.get_facts_by_attribute(attribute, self.cardinality(attribute))[-1]

    def get_facts_by_attribute(self, attribute: str, cardinality: str) -> list:
        # Filter facts by attribute
        facts = [f for f in self.facts if f.attribute == attribute and f.added]

        if cardinality == "one":
            return [facts[-1]]  # The last one is the most recent
        elif cardinality == "many":
            return facts
        else:
            raise Exception("Invalid cardinality")

    def get_distinct_attributes(self) -> set:
        """Returns a set of distinct attributes from facts"""
        return set([a.attribute for a in self.facts])

    def cardinality(self, attribute: str) -> str:
        """Returns the cardinality of a given attribute"""
        for attr in self.schema:
            if attr[0] == attribute:
                return attr[2]


class Fact:
    """Represents a fact of an entity"""

    def __init__(self, entity, attribute, value, added=True):
        self.entity = entity
        self.attribute = attribute
        self.value = value
        self.added = added

    def __str__(self) -> str:
        return f"{self.entity} {self.attribute} {self.value}"

    def __iter__(self):
        return iter((self.entity, self.attribute, self.value, self.added))
