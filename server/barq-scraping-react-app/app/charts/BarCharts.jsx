import dynamic from "next/dynamic";
import { useEffect, useState } from 'react';
import Skeleton from 'react-loading-skeleton'
import 'react-loading-skeleton/dist/skeleton.css'
import fursonas from "@/data/fursonas.json";
import age from "@/data/age.json";
import hobbies from "@/data/hobbies.json";

const Plot = dynamic(() => import("react-plotly.js"), { ssr: false, })

const colors = ["#6ac6cb", "#f5ce77", "#f69b77", "#dbb0f0", "#89c564", "#9fbaf1", "#fc87b1" ,"#c9db79", "#a3dabc", "#b397e5", "#b3b3b3"];
const colorlist = [...colors, ...colors];

export function FursonaChart() {
    const [chartData, setChartData] = useState([]);

    useEffect(() => {
        setChartData(fursonas);
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
                            orientation: 'h',
                            marker: {
                                color: colorlist
                            },
                            text: chartData.x.map(String),

                        }
                    ]}
                    layout={{
                        yaxis: {
                            automargin: true,
                            fixedrange: true
                        },
                        xaxis: {
                            fixedrange: true
                        },
                        margin: {
                            b: 15,
                            t: 15,
                            l: 15,
                            r: 15,
                            pad: 2
                        },
                        autosize: true
                    }}
                    style={{ width: "100%", height: "400px" }}
                    config={{
                        modeBarButtonsToRemove: ['lasso2d', 'select2d'],
                        responsive: true
                    }}
                />
            ) : (
                <Skeleton height={400} enableAnimation />
            )}
        </div>
    );
}


export function AgeChart() {
    const [chartData, setChartData] = useState([]);

    useEffect(() => {
        setChartData(age);
    });

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
                            },
                            fixedrange: true
                        },
                        yaxis: {
                            title: {
                                text: 'Count'
                            },
                            fixedrange: true
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
                    config={{
                        modeBarButtonsToRemove: ['lasso2d', 'select2d']
                    }}
                />
            ) : (
                <Skeleton height={325} enableAnimation />
            )}
        </div>
    );
}


export function HobbiesChart() {
    const [chartData, setChartData] = useState([]);

    useEffect(() => {
        setChartData(hobbies);
    })

    return (
        <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm w-full h-[500px]">
            <p className="text-sm font-medium text-gray-500 uppercase tracking-wide">Hobbies</p>
            {chartData.length != 0 ? (
                <Plot
                    data={[
                        {
                            x: chartData.x,
                            y: chartData.y,
                            type: 'bar',
                            orientation: 'h',
                            marker: {
                                color: colorlist
                            },
                            text: chartData.x.map(String)
                        }
                    ]}
                    layout={{
                        yaxis: {
                            automargin: true,
                            fixedrange: true
                        },
                        xaxis: {
                            fixedrange: true
                        },
                        margin: {
                            b: 15,
                            t: 15,
                            l: 15,
                            r: 15,
                            pad: 2
                        }
                    }}
                    style={{ width: "100%", height: "400px" }}
                    config={{
                        modeBarButtonsToRemove: ['lasso2d', 'select2d']
                    }}
                />
            ) : (
                <Skeleton height={400} enableAnimation />
            )}
        </div>
    );
}