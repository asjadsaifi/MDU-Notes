# MDU Notes | StudyShelf

MDU Notes (StudyShelf) is a study-material storefront for Maharshi Dayanand University (MDU) students. It currently lists a Physics study bundle with Unit 1 and 2 notes and a 2020 question paper for **$1.00 USD**.

Public website: [MDU Notes](https://mdu-notes-3ylgkzkawimsbtcbofzps5.streamlit.app/)

The site title and page copy describe MDU study notes, Physics notes, and previous-year question papers to help visitors and search engines understand the site. Search ranking and Google indexing are controlled by Google and cannot be guaranteed. Streamlit Community Cloud provides app hosting; it does not guarantee that Google will index or rank a Streamlit app.

## Local development

Requires Python 3.11 or newer.

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Run the tests with:

```powershell
python -m unittest discover -s tests -v
```

## Required owner setup for paid downloads

The app intentionally does not accept payments or reveal files until all secrets below are configured.

1. In Google Drive, change the Physics folder's general access from **Anyone with the link** to **Restricted**.
2. In Google Cloud Console, create/select a project, enable the Google Drive API, create a service account, and create a JSON key. Keep the JSON key private.
3. Share the restricted Physics folder with the service account's `client_email` as a Viewer. The app uses that service account to retrieve the two PDFs after payment.
4. In Razorpay, use the live API Key ID and Key Secret for an account authorized to accept international USD payments. Do not use test keys for live sales.
5. In Streamlit Community Cloud, open the app's **Settings → Secrets** and add the configuration below, replacing all placeholders with real values. Never commit this data or paste it into chat.

```toml
APP_URL = "https://mdu-notes-3ylgkzkawimsbtcbofzps5.streamlit.app/"

[razorpay]
key_id = "rzp_live_REPLACE_WITH_KEY_ID"
key_secret = "REPLACE_WITH_KEY_SECRET"

[drive]
folder_id = "1Wv3ZJr2-PKK0sefEXCEEyTaT8fNopjQP"

[gcp_service_account]
type = "service_account"
project_id = "REPLACE_WITH_PROJECT_ID"
private_key_id = "REPLACE_WITH_PRIVATE_KEY_ID"
private_key = """-----BEGIN PRIVATE KEY-----
REPLACE_WITH_PRIVATE_KEY_CONTENT
-----END PRIVATE KEY-----
"""
client_email = "REPLACE_WITH_SERVICE_ACCOUNT_EMAIL"
client_id = "REPLACE_WITH_CLIENT_ID"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "REPLACE_WITH_CLIENT_CERTIFICATE_URL"
```

Save secrets, then reboot the app. Make a small test-mode payment before enabling live sales; never put live secrets in the repository. Treat downloaded PDFs as customer data and only sell files you have permission to distribute.

## Public deployment

The app is deployed from the `asjadsaifi/MDU-Notes` GitHub repository, branch `main`, main file `app.py`. Streamlit Community Cloud rebuilds the app when the branch is updated. Its public URL is [mdu-notes-3ylgkzkawimsbtcbofzps5.streamlit.app](https://mdu-notes-3ylgkzkawimsbtcbofzps5.streamlit.app/).

In the Streamlit workspace, confirm **Settings → Sharing → This app is public and searchable**. Google may still take time to crawl it, and no setting can guarantee first-page placement for a broad search such as "MDU Notes." A custom domain and an SEO-oriented website with crawlable pages give more control, but also cannot guarantee a particular ranking.

## How paid delivery works

- Razorpay creates a fixed-amount USD payment link for the bundle.
- On return, the app verifies Razorpay's callback signature and fetches the payment link from Razorpay's API to confirm the amount, currency, paid status, and product.
- Only then does the app use its private Google service-account access to offer the two PDFs for download.
- The Drive folder must remain restricted; do not put public Drive file links on the product page.
