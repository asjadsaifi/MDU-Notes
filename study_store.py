from __future__ import annotations

from typing import Any


PRODUCTS: list[dict[str, Any]] = [
    {"id": "physics-formula-kit", "title": "Physics Formula Revision Kit", "subject": "Physics", "kind": "Notes", "level": "Grade 12", "price": 149, "rating": "4.9", "icon": "⚛️", "color": "#e6efe1"},
    {"id": "biology-diagrams", "title": "Biology: 50 Must-Know Diagrams", "subject": "Biology", "kind": "Notes", "level": "Grade 11–12", "price": 99, "rating": "4.8", "icon": "🌿", "color": "#eaf0dc"},
    {"id": "maths-past-papers", "title": "Mathematics Past Paper Pack", "subject": "Mathematics", "kind": "Question Papers", "level": "Grade 12", "price": 199, "rating": "4.9", "icon": "∑", "color": "#e1e9f4"},
    {"id": "chemistry-crash-course", "title": "Organic Chemistry Crash Notes", "subject": "Chemistry", "kind": "Notes", "level": "Grade 12", "price": 129, "rating": "4.7", "icon": "🧪", "color": "#f4e8d9"},
    {"id": "commerce-board-bundle", "title": "Commerce Board Exam Bundle", "subject": "Commerce", "kind": "Study Bundles", "level": "Grade 12", "price": 249, "rating": "5.0", "icon": "📈", "color": "#e8e4f2"},
    {"id": "english-literature-guide", "title": "English Literature Quick Guide", "subject": "English", "kind": "Notes", "level": "Grade 10", "price": 89, "rating": "4.6", "icon": "📖", "color": "#f4e3e1"},
    {"id": "science-mock-exams", "title": "Science Mock Exam Set · 2025", "subject": "Science", "kind": "Question Papers", "level": "Grade 10", "price": 179, "rating": "4.8", "icon": "📝", "color": "#e0efed"},
    {"id": "calculus-study-pack", "title": "Calculus Concepts & Practice", "subject": "Mathematics", "kind": "Study Bundles", "level": "Grade 11–12", "price": 219, "rating": "4.9", "icon": "∫", "color": "#f3ecd9"},
    {"id": "history-revision-notes", "title": "Modern History Revision Notes", "subject": "History", "kind": "Notes", "level": "Grade 12", "price": 119, "rating": "4.7", "icon": "🏛️", "color": "#eee5dc"},
]

CATEGORIES = ["All resources", "Notes", "Question Papers", "Study Bundles"]


def filter_products(
    products: list[dict[str, Any]],
    search_term: str = "",
    category: str = "All resources",
    sort_order: str = "Featured",
) -> list[dict[str, Any]]:
    query = search_term.strip().casefold()
    results = [
        product
        for product in products
        if (category == "All resources" or product["kind"] == category)
        and (
            not query
            or query in product["title"].casefold()
            or query in product["subject"].casefold()
            or query in product["level"].casefold()
        )
    ]
    if sort_order == "Price: low to high":
        results.sort(key=lambda product: product["price"])
    elif sort_order == "Price: high to low":
        results.sort(key=lambda product: product["price"], reverse=True)
    return results


def cart_total(cart: dict[str, int], products: list[dict[str, Any]]) -> int:
    prices = {product["id"]: product["price"] for product in products}
    return sum(prices[product_id] * quantity for product_id, quantity in cart.items() if product_id in prices)
