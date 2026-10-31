from __future__ import annotations

from typing import Any

import requests
from google.auth.exceptions import GoogleAuthError
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError


PHYSICS_BUNDLE: dict[str, Any] = {
    "id": "mdu-physics-bundle",
    "title": "Physics Unit 1 & 2 Notes + 2020 Question Paper",
    "amount_minor": 100,
    "currency": "USD",
    "folder_id": "1Wv3ZJr2-PKK0sefEXCEEyTaT8fNopjQP",
}

EXPECTED_FILES = {
    "physics.unit 1 and 2",
    "questionpaper2020",
}
DRIVE_SCOPE = "https://www.googleapis.com/auth/drive.readonly"
DRIVE_FILES_URL = "https://www.googleapis.com/drive/v3/files"


class DeliveryConfigurationError(RuntimeError):
    pass


class DeliveryError(RuntimeError):
    pass


def _drive_session() -> AuthorizedSession:
    try:
        service_account_info = dict(st.secrets["gcp_service_account"])
        drive_settings = st.secrets["drive"]
    except (StreamlitSecretNotFoundError, KeyError) as error:
        raise DeliveryConfigurationError("Google Drive delivery credentials are missing.")
    folder_id = drive_settings.get("folder_id")
    if not folder_id:
        raise DeliveryConfigurationError("Google Drive folder ID is missing.")
    try:
        credentials = service_account.Credentials.from_service_account_info(
            service_account_info,
            scopes=[DRIVE_SCOPE],
        )
    except (GoogleAuthError, ValueError, KeyError) as error:
        raise DeliveryConfigurationError("Google Drive service-account credentials are invalid.") from error
    return AuthorizedSession(credentials)


def load_paid_files() -> list[tuple[str, bytes]]:
    session = _drive_session()
    folder_id = st.secrets["drive"]["folder_id"]
    try:
        response = session.get(
            DRIVE_FILES_URL,
            params={
                "q": f"'{folder_id}' in parents and trashed = false and mimeType = 'application/pdf'",
                "fields": "nextPageToken,files(id,name,mimeType)",
                "pageSize": 100,
            },
            timeout=30,
        )
    except requests.RequestException as error:
        raise DeliveryError("Google Drive could not be reached to list the private folder.") from error
    if not response.ok:
        raise DeliveryError(f"Google Drive could not list the private folder (HTTP {response.status_code}).")

    files = response.json().get("files", [])
    matching = {
        item["name"].casefold().removesuffix(".pdf"): item
        for item in files
        if item.get("mimeType") == "application/pdf" and item.get("name")
    }
    if not EXPECTED_FILES.issubset(matching):
        raise DeliveryError("The private folder is missing one or more expected PDF files.")

    downloads: list[tuple[str, bytes]] = []
    for expected_name in sorted(EXPECTED_FILES):
        file_info = matching[expected_name]
        file_name = file_info["name"]
        if not file_name.casefold().endswith(".pdf"):
            file_name = f"{file_name}.pdf"
        try:
            download_response = session.get(
                f"{DRIVE_FILES_URL}/{file_info['id']}",
                params={"alt": "media"},
                timeout=60,
            )
        except requests.RequestException as error:
            raise DeliveryError(f"Google Drive could not be reached to download {file_name}.") from error
        if not download_response.ok:
            raise DeliveryError(f"Google Drive could not download {file_name} (HTTP {download_response.status_code}).")
        downloads.append((file_name, download_response.content))
    return downloads
