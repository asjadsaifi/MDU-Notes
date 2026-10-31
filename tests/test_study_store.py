import unittest

from study_store import PRODUCTS, cart_total, filter_products


class StudyStoreTests(unittest.TestCase):
    def test_search_matches_title_subject_and_level_without_case_sensitivity(self):
        self.assertEqual([item["id"] for item in filter_products(PRODUCTS, "BIOLOGY")], ["biology-diagrams"])
        self.assertEqual(len(filter_products(PRODUCTS, "grade 10")), 2)

    def test_category_filters_products(self):
        papers = filter_products(PRODUCTS, category="Question Papers")
        self.assertEqual({item["kind"] for item in papers}, {"Question Papers"})

    def test_price_sort_orders_products(self):
        ascending = filter_products(PRODUCTS, sort_order="Price: low to high")
        descending = filter_products(PRODUCTS, sort_order="Price: high to low")
        self.assertLessEqual(ascending[0]["price"], ascending[-1]["price"])
        self.assertGreaterEqual(descending[0]["price"], descending[-1]["price"])

    def test_cart_total_counts_quantities_and_ignores_unknown_products(self):
        self.assertEqual(
            cart_total({"physics-formula-kit": 2, "unknown": 3}, PRODUCTS),
            298,
        )


if __name__ == "__main__":
    unittest.main()
