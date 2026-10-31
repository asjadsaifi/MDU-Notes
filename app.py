from __future__ import annotations

import streamlit as st

from study_store import CATEGORIES, PRODUCTS, cart_total, filter_products


st.set_page_config(page_title="StudyShelf | Student notes & papers", page_icon="📚", layout="wide")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
    :root { --ink: #1c3028; --muted: #68776e; --green: #245c43; --lime: #d7ed9f; --paper: #f7f8f3; --line: #e7e9e1; }
    .stApp { background: var(--paper); color: var(--ink); font-family: 'DM Sans', sans-serif; }
    [data-testid="stHeader"] { background: transparent; }
    .block-container { max-width: 1220px; padding-top: 1.5rem; padding-bottom: 3rem; }
    h1, h2, h3 { color: var(--ink); font-family: 'Manrope', sans-serif; letter-spacing: -0.035em; }
    .brand { color: var(--green); font-family: 'Manrope', sans-serif; font-size: 1.2rem; font-weight: 800; letter-spacing: -0.05em; }
    .top-note { color: var(--muted); font-size: .88rem; padding-top: .5rem; }
    .hero { border-radius: 22px; padding: 2.8rem 3rem; background: #e9f0e2; position: relative; overflow: hidden; }
    .hero-kicker { color: var(--green); font-size: .76rem; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; }
    .hero h1 { font-size: clamp(2.2rem, 5vw, 3.8rem); max-width: 640px; line-height: 1.08; margin: .7rem 0; }
    .hero-copy { max-width: 520px; color: #53675a; font-size: 1.03rem; line-height: 1.65; }
    .hero-mark { position: absolute; right: 7%; top: 14%; font-size: 7rem; transform: rotate(9deg); }
    .section-title { margin: 2.25rem 0 .2rem; }
    .section-subtitle { color: var(--muted); margin-bottom: 1rem; }
    .product-card { height: 100%; min-height: 255px; padding: 1.1rem; background: white; border: 1px solid var(--line); border-radius: 16px; }
    .cover { height: 100px; border-radius: 12px; display:flex; align-items:center; justify-content:center; font-size: 2.6rem; margin-bottom: .95rem; }
    .product-type { color: var(--green); font-size: .7rem; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; }
    .product-name { font-family: 'Manrope', sans-serif; font-size: 1.03rem; font-weight: 750; line-height: 1.3; min-height: 2.65rem; margin: .35rem 0; }
    .product-meta { color: var(--muted); font-size: .83rem; }
    .product-price { color: var(--ink); font-size: 1.08rem; font-weight: 750; margin-top: .7rem; }
    [data-testid="stVerticalBlockBorderWrapper"] { border-color: var(--line); }
    .stButton button, .stLinkButton a { border-radius: 9px; font-weight: 650; }
    .stButton button[kind="primary"] { background: var(--green); border-color: var(--green); }
    [data-testid="stSidebar"] { background: #fff; }
    .trust-row { color: #526459; background: white; border: 1px solid var(--line); padding: 1rem 1.2rem; border-radius: 13px; }
    @media (max-width: 700px) {
      .block-container { padding: 1rem 1rem 2rem; }
      .hero { padding: 2rem 1.4rem; }
      .hero-mark { right: 5%; top: 8%; font-size: 3.5rem; opacity: .7; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "cart" not in st.session_state:
    st.session_state.cart = {}

header_brand, header_note, header_cart = st.columns([2, 5, 1])
with header_brand:
    st.markdown('<div class="brand">✳ StudyShelf</div>', unsafe_allow_html=True)
with header_note:
    st.markdown('<div class="top-note">Good study material. Better study days.</div>', unsafe_allow_html=True)
with header_cart:
    cart_count = sum(st.session_state.cart.values())
    st.markdown(f'<div class="top-note" style="text-align:right">🛍️ {cart_count} in bag</div>', unsafe_allow_html=True)

st.markdown(
    """
    <section class="hero">
      <div class="hero-kicker">Your next study session starts here</div>
      <h1>Find your focus.<br>Find your next A.</h1>
      <div class="hero-copy">Student-made notes, revision packs, and question papers—picked to help you spend less time searching and more time learning.</div>
      <div class="hero-mark">✎</div>
    </section>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.title("Your study bag")
    cart = st.session_state.cart
    if not cart:
        st.caption("Your bag is empty. Add a resource to get started.")
    else:
        for product_id, quantity in list(cart.items()):
            product = next((item for item in PRODUCTS if item["id"] == product_id), None)
            if product is None:
                continue
            item_col, remove_col = st.columns([5, 1])
            with item_col:
                st.markdown(f"**{product['title']}**  \n₹{product['price']} × {quantity}")
            with remove_col:
                if st.button("−", key=f"remove_{product_id}", help="Remove one"):
                    if quantity <= 1:
                        del st.session_state.cart[product_id]
                    else:
                        st.session_state.cart[product_id] -= 1
                    st.rerun()
        st.divider()
        st.markdown(f"### Total · ₹{cart_total(cart, PRODUCTS):,.0f}")
        with st.form("demo_checkout"):
            email = st.text_input("Email for your digital order", placeholder="you@example.com")
            checkout = st.form_submit_button("Continue to checkout", type="primary", use_container_width=True)
            if checkout:
                if "@" not in email or email.startswith("@") or email.endswith("@"):
                    st.error("Enter a valid email address to continue.")
                else:
                    st.info("This is a storefront preview. No payment is processed and no files are delivered yet.")

st.markdown('<h2 class="section-title">The study shelf</h2>', unsafe_allow_html=True)
st.markdown('<p class="section-subtitle">A little structure goes a long way. Find something for your next study session.</p>', unsafe_allow_html=True)

search_col, category_col, sort_col = st.columns([3, 2, 2])
with search_col:
    search_term = st.text_input("Search resources", placeholder="Try “biology” or “exam papers”", label_visibility="collapsed")
with category_col:
    category = st.selectbox("Category", CATEGORIES, label_visibility="collapsed")
with sort_col:
    sort_order = st.selectbox("Sort by", ["Featured", "Price: low to high", "Price: high to low"], label_visibility="collapsed")

visible_products = filter_products(PRODUCTS, search_term, category, sort_order)
st.caption(f"{len(visible_products)} resources")

if not visible_products:
    st.info("No resources match that search. Try another subject or choose a different category.")
else:
    for row_start in range(0, len(visible_products), 3):
        columns = st.columns(3, gap="medium")
        for column, product in zip(columns, visible_products[row_start : row_start + 3]):
            with column:
                st.markdown(
                    f"""
                    <div class="product-card">
                      <div class="cover" style="background:{product['color']}">{product['icon']}</div>
                      <div class="product-type">{product['kind']} · {product['level']}</div>
                      <div class="product-name">{product['title']}</div>
                      <div class="product-meta">{product['subject']} &nbsp;·&nbsp; ★ {product['rating']}</div>
                      <div class="product-price">₹{product['price']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if st.button("Add to bag", key=f"add_{product['id']}", type="primary", use_container_width=True):
                    st.session_state.cart[product["id"]] = st.session_state.cart.get(product["id"], 0) + 1
                    st.rerun()

st.markdown(
    """
    <div class="trust-row">
      📄 <strong>Instant-ready study resources</strong> &nbsp;&nbsp; · &nbsp;&nbsp;
      🎓 Made for students &nbsp;&nbsp; · &nbsp;&nbsp;
      🔒 Secure checkout coming soon
    </div>
    """,
    unsafe_allow_html=True,
)
st.caption("StudyShelf is a storefront demo. Product listings are sample content; checkout, payments, and downloads are not connected.")
