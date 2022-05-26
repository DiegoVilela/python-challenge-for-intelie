import unittest

from models import Entity, Fact


class EntityModelTest(unittest.TestCase):
    def setUp(self):
        self.JOAO_FACTS = [
            Fact("joão", "endereço", "rua alice, 10", True),
            Fact("joão", "endereço", "rua bob, 88", True),
            Fact("joão", "telefone", "234-5678", True),
            Fact("joão", "telefone", "91234-5555", True),
            Fact("joão", "telefone", "234-5678", False),
        ]
        self.GABRIEL_FACTS = [
            Fact("gabriel", "endereço", "av rio branco, 109", True),
            Fact("gabriel", "telefone", "98888-1111", True),
            Fact("gabriel", "telefone", "56789-1010", True),
        ]
        self.SCHEMA = [
            ("endereço", "cardinality", "one"),
            ("telefone", "cardinality", "many"),
        ]
        self.entity = Entity("gabriel", self.GABRIEL_FACTS, self.SCHEMA)

    def test_facts_attribute(self):
        """
        Entity.facts should be a list of Fact objects according to the given schema.
        """

        self.assertEqual(len(self.entity.facts), 3)

        # Fact.entity
        for fact in self.entity.facts:
            self.assertEqual(fact.entity, "gabriel")

        # Fact.attribute
        attributes = ["endereço", "telefone", "telefone"]
        for idx, attr in enumerate(attributes):
            self.assertEqual(self.entity.facts[idx].attribute, attr)

        # Fact.value
        values = ["av rio branco, 109", "98888-1111", "56789-1010"]
        for idx, value in enumerate(values):
            self.assertEqual(self.entity.facts[idx].value, value)

        # Fact.added
        for fact in self.entity.facts:
            self.assertTrue(fact.added)

    def test_fresh_facts_attribute(self):
        """
        Entity.fresh_facts should be a list of Fact objects according to the given schema.
        """
        # This fact should not appear in fresh_facts as the schema defines a cardinality
        # 'one' to 'endereço'
        self.entity.facts.append(Fact("gabriel", "endereço", "Rua Sete, 7", True))
        self.assertEqual(len(self.entity.fresh_facts), 3)

    def test_fresh_facts_attribute_with_removed_fact(self):
        """
        Entity.fresh_facts should not contain removed facts.
        """
        removed_fact = Fact("gabriel", "endereço", "Rua Sete, 7", False)
        self.entity.facts.append(removed_fact)
        facts = [tuple(fact) for fact in self.entity.fresh_facts]

        self.assertEqual(len(facts), 3)
        self.assertNotIn(removed_fact, facts)

    def test_fresh_facts_returns_last_item_when_cardinality_one(self):
        """
        Entity.fresh_facts should return the last item when cardinality is one.
        """
        self.entity.facts.extend(self.JOAO_FACTS)
        old_fact = ("joão", "endereço", "rua alice, 10", True)
        facts = [tuple(fact) for fact in self.entity.fresh_facts]
        self.assertNotIn(old_fact, facts)

    def test_fresh_facts_returns_all_facts_when_cardinality_many(self):
        """
        Entity.fresh_facts should return all facts when cardinality is many.
        """
        joao_phone1 = ("joão", "telefone", "234-5678", True)
        joao_phone2 = ("joão", "telefone", "91234-5555", True)
        joao_phone3 = ("joão", "telefone", "234-5678", False)

        self.entity.facts.extend(self.JOAO_FACTS)
        facts = [tuple(fact) for fact in self.entity.fresh_facts]

        self.assertIn(joao_phone1, facts)
        self.assertIn(joao_phone2, facts)
        self.assertNotIn(joao_phone3, facts)


if __name__ == "__main__":
    unittest.main()
