"use client";

import { MapContainer, TileLayer } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import { LanguageMarkers } from "./LanguageMarkers";
import type { BahasaMarker } from "@/lib/types";

interface LanguageMapProps {
  markers: BahasaMarker[];
  center?: [number, number];
  zoom?: number;
}

export function LanguageMap({ markers, center = [-2.5, 118.0], zoom = 5 }: LanguageMapProps) {
  return (
    <MapContainer
      center={center}
      zoom={zoom}
      className="w-full h-full"
      zoomControl={false}
    >
      <TileLayer
        attribution='&copy; <a href="https://carto.com/">CARTO</a>'
        url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png"
      />
      <LanguageMarkers markers={markers} />
    </MapContainer>
  );
}
