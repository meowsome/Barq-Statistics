import React, { useEffect, useState, useRef } from "react";
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import 'leaflet.heat'
import countries_geojson from './data/countries.json'

const chartColors = ['#FF6633', '#FFB399', '#FF33FF', '#FFFF99', '#00B3E6', 
		  '#E6B333', '#3366E6', '#999966', '#99FF99', '#B34D4D',
		  '#80B300', '#809900', '#E6B3B3', '#6680B3', '#66991A', 
		  '#FF99E6', '#CCFF1A', '#FF1A66', '#E6331A', '#33FFCC',
		  '#66994D', '#B366CC', '#4D8000', '#B33300', '#CC80CC', 
		  '#66664D', '#991AFF', '#E666FF', '#4DB3FF', '#1AB399',
		  '#E666B3', '#33991A', '#CC9999', '#B3B31A', '#00E680', 
		  '#4D8066', '#809980', '#E6FF80', '#1AFF33', '#999933',
		  '#FF3380', '#CCCC00', '#66E64D', '#4D80CC', '#9900B3', 
		  '#E64D66', '#4DB380', '#FF4D4D', '#99E6E6', '#6666FF'];

// Style for countries on the main map
function style(feature) {
    return {
        stroke: false,
        fillOpacity: 0.5
    };
}

export default function Map() {
    const [points, setPoints] = useState("");
    const isInitialized = useRef(false);
    const [visibleLayer, setVisibleLayer] = useState();
    const [map, setMap] = useState();
    const [menuOpen, setMenuOpen] = useState(false);

    function removeActiveLayer() {
        if (visibleLayer) visibleLayer.remove();
    }

    function addHeatmapLayer(localMap) {
        removeActiveLayer();

        fetch("/api/coordinates", { cache: 'force-cache' })
        .then((res) => res.json())
        .then((data) => {
            setPoints(data)
            const heatLayer = L.heatLayer(data, {minOpacity: 0.3}).addTo(localMap ? localMap : map);
            setVisibleLayer(heatLayer);
        });
    }

    function addFursonaLayer() {
        removeActiveLayer();

        fetch("/api/sonas-per-country", { cache: 'force-cache' })
        .then((res) => res.json())
        .then((data) => {
            const uniqueSonas = [...new Set(data.map(country => country.popularFursona))];
            let sonasColors = {};
            for (let i = 0; i < uniqueSonas.length; i++) {
                sonasColors[uniqueSonas[i]] = chartColors[i];
            }

            const fursonaLayer = L.geoJson(countries_geojson, {
                onEachFeature: function(feature, layer) {
                    var countryName = feature.properties.name;
                    const countryDetails = data.find(country => country._id == countryName || country._id == "United States" && countryName == "United States of America"); 
                    if (countryDetails != null) {
                        const popularFursona = countryDetails.popularFursona;
                        layer.setStyle({
                            fillColor: sonasColors[popularFursona]
                        })
                        layer.bindTooltip("<b>" + popularFursona + "</b>", {permanent: true});
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
            
            <div className="absolute top-3 right-3 z-1 text-right">
                <button data-dropdown-toggle="dropdown" className="inline-flex items-center justify-center text-black shadow-xs font-medium leading-5 rounded-base text-sm px-4 py-2.5 cursor-pointer bg-white" type="button" onClick={() => setMenuOpen(!menuOpen)}>
                    Map Layers
                    <svg className="w-4 h-4 ms-1.5 -me-0.5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24"><path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="m19 9-7 7-7-7"/></svg>
                </button>

                {menuOpen && (
                    <div id="dropdown" className="z-10 bg-neutral-primary-medium rounded-base shadow-lg w-50 bg-white">
                        <ul className="p-2 text-sm text-body font-medium" aria-labelledby="dropdownDefaultButton">
                            <li>
                                <a className="inline-flex items-center w-full p-2 hover:bg-neutral-tertiary-medium hover:text-heading rounded cursor-pointer" onClick={() => addHeatmapLayer()}>Furry Locations Heatmap</a>
                            </li>
                            <li>
                                <a className="inline-flex items-center w-full p-2 hover:bg-neutral-tertiary-medium hover:text-heading rounded cursor-pointer" onClick={() => addFursonaLayer()}>Top Fursona Per Country</a>
                            </li>
                        </ul>
                    </div>
                )}
            </div>
        </div>
    );
}
