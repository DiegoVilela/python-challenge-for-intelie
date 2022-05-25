from models import Entity, Fact


def distinct_entities(facts: list) -> set:
    """Returns a set of entities from facts based on the first element of each tuple"""
    return set([fact[0] for fact in facts])


def get_facts_by_entity(facts, entity):
    """Returns a list of Fact objects of a given entity"""
    return [Fact(*fact) for fact in facts if fact[0] == entity]


def get_entities(facts: list, schema: list) -> set:
    """Returns a set of Entity objects of a given list of facts"""
    entities = set()
    for entity in distinct_entities(facts):
        # Create each Entity with all its facts
        entities.add(Entity(entity, get_facts_by_entity(facts, entity), schema))

    return entities


def get_fresh_facts(facts: list, schema: list) -> list:
    """Returns a list of in force Fact objects from a given list of facts based on a given schema"""
    fresh = []
    for entity in get_entities(facts, schema):
        fresh.extend(entity.fresh_facts)

    return fresh
