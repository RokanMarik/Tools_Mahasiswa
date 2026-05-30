"""Collection selection UI for Zotero."""

from typing import Optional, Dict, List


class CollectionPicker:
    def __init__(self, client):
        """Initialize with a ZoteroClient instance."""
        self.client = client
        self._collections = []

    def display_collections(self) -> str:
        """Fetch and format collection list for display.

        Returns:
            Formatted string of collections.
        """
        self._collections = self.client.get_collections()

        if not self._collections:
            return "Tidak ada koleksi ditemukan. Pastikan library Zotero kamu tidak kosong."

        lines = ["Koleksi Zotero kamu:"]
        for i, coll in enumerate(self._collections, 1):
            lines.append(f"  {i}. {coll['name']} ({coll['num_items']} items)")

        return "\n".join(lines)

    def select_by_number(self, number: int) -> Optional[Dict]:
        """Select collection by list number (1-indexed)."""
        if not self._collections:
            self._collections = self.client.get_collections()

        if number < 1 or number > len(self._collections):
            return None

        return self._collections[number - 1]

    def select_by_name(self, name: str) -> Optional[Dict]:
        """Select collection by name (case-insensitive partial match)."""
        if not self._collections:
            self._collections = self.client.get_collections()

        name_lower = name.lower()
        for coll in self._collections:
            if name_lower in coll["name"].lower():
                return coll

        return None

    def pick(self) -> Optional[Dict]:
        """Interactive collection picker.

        Returns:
            Selected collection dict or None if cancelled.
        """
        print(self.display_collections())
        print()
        print("Pilih nomor (atau ketik nama koleksi): ", end="")

        try:
            user_input = input().strip()
        except (EOFError, KeyboardInterrupt):
            print("\nDibatalkan.")
            return None

        if not user_input:
            print("Dibatalkan.")
            return None

        # Try number first
        if user_input.isdigit():
            result = self.select_by_number(int(user_input))
            if result:
                return result
            print(f"Nomor {user_input} tidak ada. Coba lagi.")
            return None

        # Try name
        result = self.select_by_name(user_input)
        if result:
            return result

        print(f"Koleksi '{user_input}' tidak ditemukan. Ketik 'list' untuk lihat semua koleksi.")
        return None
