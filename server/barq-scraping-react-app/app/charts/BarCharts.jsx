import dynamic from "next/dynamic";
import { useEffect, useState } from 'react';
import Skeleton from 'react-loading-skeleton'
import 'react-loading-skeleton/dist/skeleton.css'

const Plot = dynamic(() => import("react-plotly.js"), { ssr: false, })

export function FursonaChart() {
    const [chartData, setChartData] = useState([]);

    useEffect(() => {
        fetch("/api/fursonas")
        .then((res) => res.json())
        .then((data) => {
            setChartData(data);
        });
    })

    return (
        <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm w-full h-[500px]">
            <p className="text-sm font-medium text-gray-500 uppercase tracking-wide">Fursona</p>
            {chartData.length != 0 ? (
                <Plot
                    data={[
                        {
                            x: chartData.x,
                            y: chartData.y,
                            type: 'bar',
                            orientation: 'h'
                        }
                    ]}
                    layout={{
                        yaxis: {
                            automargin: true,
                        },
                        margin: {
                            b: 20,
                            t: 20,
                            pad: 0
                        }
                    }}
                    style={{ width: "100%", height: "400px" }}
                />
            ) : (
                <Skeleton height={500} enableAnimation />
            )}
        </div>
    );
}


export function AgeChart() {
    const [chartData, setChartData] = useState([]);

    useEffect(() => {
        fetch("/api/age")
        .then((res) => res.json())
        .then((data) => {
            setChartData(data);
        });
    })

    return (
        <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm w-full h-[400px]">
            <p className="text-sm font-medium text-gray-500 uppercase tracking-wide">Distribution of Ages</p>
            {chartData.length != 0 ? (
                <Plot
                    data={[
                        {
                            x: chartData,
                            type: 'histogram',
                        }
                    ]}
                    
                    layout={{
                        xaxis: {
                            title: {
                                text: 'Age'
                            }
                        },
                        yaxis: {
                            title: {
                                text: 'Count'
                            }
                        },
                        margin: {
                            b: 50,
                            t: 15,
                            l: 50,
                            r: 15,
                            pad: 0
                        }
                    }}
                    style={{ width: "100%", height: "325px" }}
                />
            ) : (
                <Skeleton height={325} enableAnimation />
            )}
        </div>
    );
}