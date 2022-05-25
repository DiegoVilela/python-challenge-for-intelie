from data import facts, schema
from utils import get_fresh_facts

current_facts = get_fresh_facts(facts, schema)

if __name__ == '__main__':
    for fact in current_facts:
        print(tuple(fact)) # Prints facts represented as tuples
