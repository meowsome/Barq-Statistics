import React, { useEffect, useState, useRef } from "react";
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import 'leaflet.heat'

export default function Map() {
    const [points, setPoints] = useState("");
    const isInitialized = useRef(false);
    const [visibleLayer, setVisibleLayer] = useState();
    const [map, setMap] = useState();

    function removeActiveLayer() {
        if (visibleLayer) visibleLayer.remove();
    }

    function addHeatmapLayer(localMap) {
        removeActiveLayer();

        fetch("/api/coordinates")
        .then((res) => res.json())
        .then((data) => {
            setPoints(data)
            const heatLayer = L.heatLayer(data, {minOpacity: 0.3}).addTo(localMap ? localMap : map);
            setVisibleLayer(heatLayer);
        });
    }

    function addFursonaLayer() {
        removeActiveLayer();

        fetch("/api/sonas-per-country")
        .then((res) => res.json())
        .then((data) => {
            const uniqueSonas = [...new Set(data.map(country => country.popularFursona))];
            let sonasColors = {};
            for (let i = 0; i < uniqueSonas.length; i++) {
                sonasColors[uniqueSonas[i]] = chartColors[i];
            }
            
            console.log(uniqueSonas)
            console.log(sonasColors)

            const fursonaLayer = L.geoJson(countries_geojson, {
                onEachFeature: function(feature, layer) {
                    var countryName = feature.properties.name;
                    const countryDetails = data.find(country => country._id == countryName);
                    if (countryDetails != null) {
                        const popularFursona = countryDetails.popularFursona;
                        console.log(sonasColors[popularFursona]);
                        layer.setStyle({
                            fillColor: sonasColors[popularFursona]
                        })
                        layer.bindPopup("<b>" + popularFursona + "</b>");
                    }
                },
                style: style
            }).addTo(map);
            
            setVisibleLayer(fursonaLayer);
        })
    }

    // Initialize map, only run once
    useEffect(() => {
        // In dev, map gets initialized twice and creates error
        if (!isInitialized.current) {
            const map = L.map("map").setView([40.7128, -74.0060], 5);
            L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
            attribution:
                '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(map);

            setMap(map);

            
            addHeatmapLayer(map);
        }
        
        isInitialized.current = true;
    }, []);

    return (
        <div>
            <div className="relative z-0" id="map" style={{ height: "100vh", width: "100%" }}></div>
            
            <div className="absolute top-3 right-3 z-1">
                <button className="bg-blue-500 text-white" onClick={() => addHeatmapLayer()}>Heatmap Layer</button>&nbsp;
                <button className="bg-blue-500 text-white" onClick={() => addFursonaLayer()}>Fursona Layer</button>
            </div>
        </div>
    );
}
