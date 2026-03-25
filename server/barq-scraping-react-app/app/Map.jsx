import React, { useEffect, useState, useRef } from "react";
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import 'leaflet.heat'

export default function Map() {
    const [points, setPoints] = useState("");
    const isInitialized = useRef(false);

    useEffect(() => {
        // In dev, map gets initialized twice and creates error        
        if (!isInitialized.current) {        
            const map = L.map("map").setView([40.7128, -74.0060], 5);
            L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
            attribution:
                '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(map);

            // Fetch all coords from backend
            fetch(process.env.API_FETCH_COORDS)
            .then((res) => res.json())
            .then((data) => {
                setPoints(data)

                // Add coords as heatmap as layer on leaflet map
                L.heatLayer(data, {minOpacity: 0.3}).addTo(map);
            })
        }
        
        isInitialized.current = true;
    }, []);

    return <div id="map" style={{ height: "100vh", width: "100%" }}></div>;
}
