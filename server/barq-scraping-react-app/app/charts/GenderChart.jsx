import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { useEffect, useState } from 'react';
import { Pie } from 'react-chartjs-2';
import ChartDataLabels from "chartjs-plugin-datalabels";
import Skeleton from 'react-loading-skeleton'
import 'react-loading-skeleton/dist/skeleton.css'

ChartJS.register(ArcElement, Tooltip, Legend, ChartDataLabels);

export default function GenderChart() {
    const [chartData, setChartData] = useState({ labels: [], datasets: [] });

    useEffect(() => {
        fetch("process.env.API_FETCH_GENDERS")
        .then((res) => res.json())
        .then((data) => {
            setChartData({
                labels: data.labels,
                datasets: [{
                    data: data.counts
                }]
            });
        });
    })

    return (
        <div>
            <h2 className="font-medium text-lg">Gender</h2>
            {chartData.datasets.length > 0 ? (
                <Pie data={chartData} />
            ) : (
                <Skeleton circle height="500" enableAnimation />
            )}
        </div>
    );
}