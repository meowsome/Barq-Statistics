import dynamic from "next/dynamic";
import { useEffect, useState } from 'react';
import Skeleton from 'react-loading-skeleton'
import 'react-loading-skeleton/dist/skeleton.css'

const Plot = dynamic(() => import("react-plotly.js"), { ssr: false, })

const chartLayout = {
    autosize: true,
    margin: { l: 55, r: 0, b: 0, t: 0, pad: 0},
    showlegend: true,
    legend: {
        yanchor: "center",
        y: 0.5,
        xanchor: "right",
        x: 2
    }
}

const chartStyle = { width: "100%", height: "100%" }

export function GenderChart() {
    const [chartData, setChartData] = useState({});

    useEffect(() => {
        fetch("/api/genders")
        .then((res) => res.json())
        .then((data) => {
            setChartData(data);
        });
    })

    return (
        <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm w-full">
            <p className="text-sm font-medium text-gray-500 uppercase tracking-wide">Gender</p>
            {"values" in chartData ? (
                <div style={{ width: '100%', height: '200px' }}>
                    <Plot
                        data={[
                            {
                                values: chartData.values,
                                labels: chartData.labels,
                                type: 'pie',
                                textinfo: "percent"
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
        fetch("/api/orientation")
        .then((res) => res.json())
        .then((data) => {
            setChartData(data);
        });
    })

    return (
        <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm w-full">
            <p className="text-sm font-medium text-gray-500 uppercase tracking-wide">Orientation</p>
            {"values" in chartData ? (
                <div style={{ width: '100%', height: '200px' }}>
                    <Plot
                        data={[
                            {
                                values: chartData.values,
                                labels: chartData.labels,
                                type: 'pie',
                                textinfo: "percent"
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
        fetch("/api/relationship")
        .then((res) => res.json())
        .then((data) => {
            setChartData(data);
        });
    })

    return (
        <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm w-full">
            <p className="text-sm font-medium text-gray-500 uppercase tracking-wide">Relationships</p>
            {"values" in chartData ? (
                <div style={{ width: '100%', height: '275px' }}>
                    <Plot
                        data={[
                            {
                                values: chartData.values,
                                labels: chartData.labels,
                                type: 'pie',
                                textinfo: "percent"
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
