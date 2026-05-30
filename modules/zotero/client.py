"""Zotero Web API client wrapper."""

import os
import time
import requests
from typing import List, Dict, Optional

ZOTERO_API_BASE = "https://api.zotero.org"
DEFAULT_LIMIT = 100
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds


class ZoteroClient:
    def __init__(
        self,
        api_key: str,
        library_type: str = "users",
        library_id: Optional[str] = None,
    ):
        """Initialize Zotero API client.

        Args:
            api_key: Zotero API key.
            library_type: 'users' for personal library, 'groups' for group library.
            library_id: User ID or group ID. If None, will auto-detect for 'users'.
        """
        self.api_key = api_key
        self.library_type = library_type
        self.library_id = library_id or "0"  # 0 = current user
        self.base_url = ZOTERO_API_BASE
        self.headers = {
            "Zotero-API-Key": self.api_key,
            "Content-Type": "application/json",
        }

    def _get(self, endpoint: str, params: Optional[Dict] = None) -> requests.Response:
        """Make GET request with retry on rate limit."""
        url = f"{self.base_url}/{endpoint}"
        params = params or {}

        for attempt in range(MAX_RETRIES):
            try:
                response = requests.get(url, headers=self.headers, params=params, timeout=30)

                if response.status_code == 503:
                    # Rate limited — wait and retry
                    if attempt < MAX_RETRIES - 1:
                        print(f"  Rate limited. Waiting {RETRY_DELAY}s...")
                        time.sleep(RETRY_DELAY)
                        continue
                    else:
                        raise Exception("Rate limited after 3 retries. Try again later.")

                response.raise_for_status()
                return response

            except requests.exceptions.ConnectionError:
                raise Exception("Tidak bisa terhubung ke Zotero API. Cek koneksi internet.")
            except requests.exceptions.Timeout:
                raise Exception("Request timeout. Cek koneksi internet.")

        raise Exception("Unexpected error in request.")

    def get_user_id(self) -> str:
        """Get the current user's ID from the API."""
        response = self._get("keys/current")
        data = response.json()
        user_id = data.get("userID")
        if user_id is None:
            raise Exception("Tidak bisa mendapatkan user ID dari API key.")
        return str(user_id)

    def get_collections(self) -> List[Dict]:
        """Get all collections in the library.

        Returns:
            List of {key, name, num_items}.
        """
        library_path = f"{self.library_type}/{self.library_id}"
        endpoint = f"{library_path}/collections"
        response = self._get(endpoint, params={"format": "json"})
        data = response.json()

        collections = []
        for item in data:
            collections.append({
                "key": item["key"],
                "name": item["data"]["name"],
                "num_items": item["meta"].get("numItems", 0),
            })

        return collections

    def get_collection_items(self, collection_key: str, limit: int = DEFAULT_LIMIT) -> List[Dict]:
        """Get all items in a collection (metadata only, no attachments).

        Args:
            collection_key: The collection key from get_collections().
            limit: Max items to fetch per request.

        Returns:
            List of {title, creators, date, doi, url, journal, item_type, key}.
        """
        library_path = f"{self.library_type}/{self.library_id}"
        endpoint = f"{library_path}/collections/{collection_key}/items"

        all_items = []
        start = 0

        while True:
            params = {
                "format": "json",
                "limit": limit,
                "start": start,
            }
            response = self._get(endpoint, params=params)
            data = response.json()

            if not data:
                break

            for item in data:
                item_data = item.get("data", {})
                item_type = item_data.get("itemType", "")

                # Skip attachments — we only want metadata
                if item_type in ("attachment", "note"):
                    continue

                creators = item_data.get("creators", [])
                authors = []
                for c in creators:
                    if c.get("creatorType") == "author":
                        name = f"{c.get('firstName', '')} {c.get('lastName', '')}".strip()
                        if name:
                            authors.append(name)

                all_items.append({
                    "key": item.get("key", ""),
                    "title": item_data.get("title", "Untitled"),
                    "authors": authors,
                    "date": item_data.get("date", ""),
                    "doi": item_data.get("DOI", ""),
                    "url": item_data.get("url", ""),
                    "journal": item_data.get("publicationTitle", ""),
                    "item_type": item_type,
                })

            if len(data) < limit:
                break

            start += limit

        return all_items

    def _post(self, endpoint: str, payload: List[Dict]) -> requests.Response:
        """Make POST request with retry on rate limit."""
        url = f"{self.base_url}/{endpoint}"

        for attempt in range(MAX_RETRIES):
            try:
                response = requests.post(
                    url,
                    headers=self.headers,
                    json=payload,
                    timeout=30,
                )

                if response.status_code == 503:
                    if attempt < MAX_RETRIES - 1:
                        print(f"  Rate limited. Waiting {RETRY_DELAY}s...")
                        time.sleep(RETRY_DELAY)
                        continue
                    else:
                        raise Exception("Rate limited after 3 retries.")

                response.raise_for_status()
                return response

            except requests.exceptions.ConnectionError:
                raise Exception("Tidak bisa terhubung ke Zotero API. Cek koneksi internet.")
            except requests.exceptions.Timeout:
                raise Exception("Request timeout. Cek koneksi internet.")

        raise Exception("Unexpected error in request.")

    def create_collection(self, name: str, parent_key: str = None) -> Dict:
        """Create a new collection.

        Args:
            name: Collection name.
            parent_key: Parent collection key (None for top-level).

        Returns:
            {key, name, version}.
        """
        library_path = f"{self.library_type}/{self.library_id}"
        endpoint = f"{library_path}/collections"

        payload = [{
            "name": name,
            "parentCollection": parent_key or "",
        }]

        response = self._post(endpoint, payload)
        result = response.json()

        # Zotero batch API returns {successful: {idx: {key, version, ...}}}
        successful = result.get("successful", {})
        if successful:
            first_key = list(successful.keys())[0]
            item = successful[first_key]
            return {
                "key": item.get("key", ""),
                "name": name,
                "version": item.get("version", 0),
            }

        # Fallback: check for errors
        failed = result.get("failed", {})
        if failed:
            first_fail = list(failed.values())[0]
            raise Exception(f"Failed: {first_fail.get('message', 'Unknown error')}")

        raise Exception("Failed to create collection — unexpected API response.")

    def add_item(self, collection_key: str, item_data: Dict) -> Dict:
        """Add a single item to a collection.

        Args:
            collection_key: Target collection key.
            item_data: Dict with keys: title, itemType, creators, date, DOI, url, publicationTitle.

        Returns:
            {key, version}.
        """
        library_path = f"{self.library_type}/{self.library_id}"
        endpoint = f"{library_path}/items"

        # Build creators format
        creators = []
        for author_name in item_data.get("creators", item_data.get("authors", [])):
            parts = author_name.strip().split()
            if len(parts) >= 2:
                creators.append({
                    "creatorType": "author",
                    "firstName": " ".join(parts[:-1]),
                    "lastName": parts[-1],
                })
            else:
                creators.append({
                    "creatorType": "author",
                    "lastName": author_name,
                })

        payload = [{
            "itemType": item_data.get("itemType", "journalArticle"),
            "title": item_data.get("title", ""),
            "creators": creators,
            "date": item_data.get("date", ""),
            "DOI": item_data.get("doi", item_data.get("DOI", "")),
            "url": item_data.get("url", ""),
            "publicationTitle": item_data.get("journal", item_data.get("publicationTitle", "")),
            "collections": [collection_key] if collection_key else [],
        }]

        response = self._post(endpoint, payload)
        result = response.json()

        # Zotero batch API returns {successful: {idx: {key, version, ...}}}
        successful = result.get("successful", {})
        if successful:
            first_key = list(successful.keys())[0]
            item = successful[first_key]
            return {
                "key": item.get("key", ""),
                "version": item.get("version", 0),
            }

        failed = result.get("failed", {})
        if failed:
            first_fail = list(failed.values())[0]
            raise Exception(f"Failed: {first_fail.get('message', 'Unknown error')}")

        raise Exception("Failed to add item — unexpected API response.")
