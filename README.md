# MDU Notes | StudyShelf

StudyShelf is a Streamlit storefront prototype for browsing sample study notes, question papers, and revision bundles.

## Run locally

Requires Python 3.11 or newer.

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Deploy publicly

1. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/) with GitHub.
2. Select **Create app**, then choose the `asjadsaifi/MDU-Notes` repository, the `main` branch, and `app.py` as the app file.
3. Choose **Deploy**. Streamlit will build the app and provide its public `*.streamlit.app` URL.

The app requires no secrets or environment variables. Search engines may take time to index a newly deployed site.

## Included features

- Search by resource title, subject, or grade.
- Filter by notes, question papers, or study bundles.
- Sort products by price.
- Add sample listings to a session-based shopping bag.

## Important limitations

This is a demo catalog, not a complete commerce service. Checkout, payments, accounts, order storage, and digital downloads are not implemented. Replace sample listings with content you are authorized to distribute and integrate a payment provider and secure order/download delivery before selling.
