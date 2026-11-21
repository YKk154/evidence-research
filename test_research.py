import unittest
from research import build, Demo, DEMO_TOPIC, Finding, Notes


class Invalid(Demo):
    def notes(self, state):
        return Notes(findings=[Finding(claim="无依据结论", quote="不存在的摘录", source=1),
                               Finding(claim="错误编号", quote="80", source=99)], followup=state["searched"][0])


class WorkflowTest(unittest.TestCase):
    def run_graph(self, provider, budget=4):
        return build(provider, budget).invoke({"topic": DEMO_TOPIC})

    def test_followup(self):
        state = self.run_graph(Demo())
        self.assertEqual((len(state["searched"]), len(state["findings"])), (2, 2))
        self.assertIn("45 毫秒", state["report"])

    def test_budget(self):
        self.assertEqual(len(self.run_graph(Demo(), 1)["searched"]), 1)

    def test_invalid_citations_and_repeated_query(self):
        state = self.run_graph(Invalid())
        self.assertEqual((state["rejected"], state["findings"], len(state["searched"])), (2, [], 1))
        self.assertIn("资料不足", state["report"])

    def test_duplicate_sources(self):
        class Duplicate(Demo):
            def search(self, query):
                return super().search(query) * 2
        self.assertEqual(len(self.run_graph(Duplicate())["sources"]), 2)

