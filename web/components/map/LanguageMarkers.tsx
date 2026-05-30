"use client";

import { Marker, Popup, useMap } from "react-leaflet";
import { Icon } from "leaflet";
import { MapPopup } from "./MapPopup";
import type { BahasaMarker } from "@/lib/types";

function createMarkerIcon(rumpunNama: string | null): Icon {
  const color = rumpunNama === "Papua" ? "#8b3a3a" : rumpunNama === "Trans-New Guinea" ? "#5a7247" : "#c4703f";
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="36" viewBox="0 0 24 36"><path d="M12 0C5.4 0 0 5.4 0 12c0 9 12 24 12 24s12-15 12-24C24 5.4 18.6 0 12 0z" fill="${color}" stroke="white" stroke-width="1.5"/><circle cx="12" cy="12" r="5" fill="white" opacity="0.9"/></svg>`;
  return new Icon({
    iconUrl: `data:image/svg+xml;base64,${btoa(svg)}`,
    iconSize: [24, 36], iconAnchor: [12, 36], popupAnchor: [0, -36],
  });
}

export function LanguageMarkers({ markers }: { markers: BahasaMarker[] }) {
  const map = useMap();
  return (
    <>
      {markers.map((m) => (
        <Marker key={m.id} position={[m.lat, m.lng]} icon={createMarkerIcon(m.rumpunNama)}
          eventHandlers={{ click: () => { map.flyTo([m.lat, m.lng], 8, { duration: 1 }); } }}>
          <Popup><MapPopup marker={m} /></Popup>
        </Marker>
      ))}
    </>
  );
}
