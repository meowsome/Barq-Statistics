import dynamic from "next/dynamic";
import { useEffect, useState } from 'react';
import Skeleton from 'react-loading-skeleton'
import 'react-loading-skeleton/dist/skeleton.css'
import genders from "@/data/genders.json";
import orientation from "@/data/orientation.json";
import relationship from "@/data/relationship.json";

const colorlist = ["#6ac6cb", "#f5ce77", "#f69b77", "#dbb0f0", "#89c564", "#9fbaf1", "#fc87b1" ,"#c9db79", "#a3dabc", "#b397e5", "#b3b3b3"];

const Plot = dynamic(() => import("react-plotly.js"), { ssr: false, })

const chartLayout = {
    autosize: true,
    margin: {
        t: 20,
        l: 20,
        r: 20,
        b: 50,
    },
    showlegend: true,
    legend: {
        orientation: "h",
        x: 0.5,
        xanchor: "center",
        y: 1.1,
        yanchor: "bottom",
    },
    colorway: colorlist
}

const chartStyle = { width: "100%", height: "100%" }

export function GenderChart() {
    const [chartData, setChartData] = useState({});

    useEffect(() => {
        setChartData(genders);
    })

    return (
        <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm w-full">
            <p className="text-sm font-medium text-gray-500 uppercase tracking-wide">Gender</p>
            {"values" in chartData ? (
                <div style={{ width: '100%', height: '350px' }}>
                    <Plot
                        data={[
                            {
                                values: chartData.values,
                                labels: chartData.labels,
                                type: 'pie',
                            }
                        ]}
                        layout={chartLayout}
                        useResizeHandler={true}
                        style={chartStyle}
                    />
                </div>
            ) : (
                <Skeleton height={200} enableAnimation />
            )}
        </div>
    );
}

export function OrientationChart() {
    const [chartData, setChartData] = useState({});

    useEffect(() => {
        setChartData(orientation);
    })

    return (
        <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm w-full">
            <p className="text-sm font-medium text-gray-500 uppercase tracking-wide">Orientation</p>
            {"values" in chartData ? (
                <div style={{ width: '100%', height: '350px' }}>
                    <Plot
                        data={[
                            {
                                values: chartData.values,
                                labels: chartData.labels,
                                type: 'pie',
                            }
                        ]}
                        layout={chartLayout}
                        useResizeHandler={true}
                        style={chartStyle}
                    />
                </div>
            ) : (
                <Skeleton height={200} enableAnimation />
            )}
        </div>
    );
}

export function RelationshipChart() {
    const [chartData, setChartData] = useState({});

    useEffect(() => {
        setChartData(relationship);
    })

    return (
        <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm w-full">
            <p className="text-sm font-medium text-gray-500 uppercase tracking-wide">Relationships</p>
            {"values" in chartData ? (
                <div style={{ width: '100%', height: '350px' }}>
                    <Plot
                        data={[
                            {
                                values: chartData.values,
                                labels: chartData.labels,
                                type: 'pie',
                            }
                        ]}
                        layout={chartLayout}
                        useResizeHandler={true}
                        style={chartStyle}
                    />
                </div>
            ) : (
                <Skeleton height={275} enableAnimation />
            )}
        </div>
    );
}
