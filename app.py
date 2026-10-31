from __future__ import annotations

import streamlit as st

from payments import PaymentConfigurationError, PaymentError, create_payment_link, verify_payment
from study_store import (
    DeliveryConfigurationError,
    DeliveryError,
    PHYSICS_BUNDLE,
    load_paid_files,
)


st.set_page_config(
    page_title="MDU Notes | MDU Study Notes & Question Papers",
    page_icon="📚",
    layout="wide",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
    :root { --ink: #1c3028; --muted: #68776e; --green: #245c43; --paper: #f7f8f3; --line: #e7e9e1; }
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
    .product-card { padding: 1.3rem; background: white; border: 1px solid var(--line); border-radius: 16px; }
    .cover { height: 130px; border-radius: 12px; display:flex; align-items:center; justify-content:center; font-size: 3.2rem; margin-bottom: 1rem; background: #e6efe1; }
    .product-type { color: var(--green); font-size: .72rem; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; }
    .product-name { font-family: 'Manrope', sans-serif; font-size: 1.15rem; font-weight: 750; line-height: 1.3; margin: .4rem 0; }
    .product-meta { color: var(--muted); font-size: .88rem; }
    .product-price { color: var(--ink); font-size: 1.25rem; font-weight: 750; margin-top: .8rem; }
    .stButton button, .stLinkButton a { border-radius: 9px; font-weight: 650; }
    .stButton button[kind="primary"] { background: var(--green); border-color: var(--green); }
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

brand, tagline = st.columns([1, 5])
with brand:
    st.markdown('<div class="brand">✳ MDU Notes</div>', unsafe_allow_html=True)
with tagline:
    st.markdown('<div class="top-note">StudyShelf · Good study material. Better study days.</div>', unsafe_allow_html=True)

st.markdown(
    """
    <section class="hero">
      <div class="hero-kicker">Made for your next study session</div>
      <h1>Find your focus.<br>Find your next A.</h1>
      <div class="hero-copy">Browse study notes and question papers for Maharshi Dayanand University students.</div>
      <div class="hero-mark">✎</div>
    </section>
    """,
    unsafe_allow_html=True,
)

st.markdown('<h2 class="section-title">MDU Physics notes and question papers</h2>', unsafe_allow_html=True)
st.markdown(
    '<p class="section-subtitle">StudyShelf is an MDU study-material storefront for Maharshi Dayanand University students. '
    "Browse subject notes, revision resources, and previous-year question papers for focused exam preparation.</p>",
    unsafe_allow_html=True,
)

callback = st.query_params
callback_fields = {
    "razorpay_payment_id",
    "razorpay_payment_link_id",
    "razorpay_payment_link_reference_id",
    "razorpay_payment_link_status",
    "razorpay_signature",
}

if callback_fields.issubset(callback.keys()):
    st.subheader("Checking your payment")
    try:
        paid = verify_payment(
            payment_id=callback["razorpay_payment_id"],
            payment_link_id=callback["razorpay_payment_link_id"],
            reference_id=callback["razorpay_payment_link_reference_id"],
            status=callback["razorpay_payment_link_status"],
            signature=callback["razorpay_signature"],
        )
        if not paid:
            st.error("Payment could not be verified. Your files remain locked. Please contact the store owner with your Razorpay payment receipt.")
        else:
            st.success("Payment verified.")
            try:
                for file_name, file_content in load_paid_files():
                    st.download_button(
                        f"Download {file_name}",
                        data=file_content,
                        file_name=file_name,
                        mime="application/pdf",
                        key=f"download_{file_name}",
                    )
            except DeliveryConfigurationError:
                st.error("Payment was received, but private file delivery is not configured. Contact the store owner with your Razorpay receipt.")
            except DeliveryError as error:
                st.error(f"Payment was received, but file delivery failed: {error} Contact the store owner with your Razorpay receipt.")
    except PaymentConfigurationError:
        st.error("Secure delivery is not configured yet. Please contact the store owner.")
    except PaymentError as error:
        st.error(f"Could not complete the secure payment check: {error}")
else:
    with st.container(border=True):
        st.markdown(
            f"""
            <div class="product-card">
              <div class="cover">⚛️</div>
              <div class="product-type">PDFs · Physics</div>
              <div class="product-name">{PHYSICS_BUNDLE['title']}</div>
              <div class="product-meta">Includes physics unit 1 and 2 notes and questionpaper2020.</div>
              <div class="product-price">$1.00 USD · both PDFs</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        buyer_email = st.text_input("Email for your payment receipt", placeholder="you@example.com")
        if st.button("Continue to secure Razorpay checkout · $1.00", type="primary"):
            if "@" not in buyer_email or buyer_email.startswith("@") or buyer_email.endswith("@"):
                st.error("Enter a valid email address to continue.")
            else:
                try:
                    checkout_url = create_payment_link(buyer_email)
                    st.link_button("Open Razorpay secure checkout", checkout_url, type="primary")
                    st.caption("After payment, Razorpay will return here to verify the payment and unlock the PDFs.")
                except PaymentConfigurationError:
                    st.error("Checkout is not configured yet. The store owner must finish the secure setup before accepting payments.")
                except PaymentError as error:
                    st.error(f"Could not create a checkout link: {error}")

st.markdown(
    """
    <div class="trust-row">
      📄 Two Physics PDFs &nbsp;&nbsp; · &nbsp;&nbsp;
      💳 Secure checkout via Razorpay &nbsp;&nbsp; · &nbsp;&nbsp;
      🔒 Files unlock only after payment verification
    </div>
    """,
    unsafe_allow_html=True,
)
st.caption("Digital materials are delivered after Razorpay confirms successful payment. Please purchase only for personal study.")

st.divider()
st.subheader("About MDU Notes")
st.write(
    "MDU Notes is a study-material collection for students of Maharshi Dayanand University (MDU), "
    "also known as MDU Rohtak. Find MDU study notes, subject revision material, and previous-year "
    "question papers in one place. The current listing is a Physics bundle with Unit 1 and 2 notes "
    "and a 2020 question paper."
)
with st.expander("What is included in the Physics study bundle?"):
    st.write(
        "The bundle contains two PDFs: Physics Unit 1 and 2 notes, plus the 2020 Physics question paper."
    )
with st.expander("Who is MDU Notes for?"):
    st.write(
        "The materials are intended for MDU students looking for Physics notes and question-paper "
        "practice. Check your course and syllabus before studying from any resource."
    )
with st.expander("How do I access the PDFs?"):
    st.write(
        "The bundle is listed for $1.00 USD. Secure checkout and private PDF delivery will be available "
        "after the store owner completes the Razorpay and Google Drive setup."
    )
