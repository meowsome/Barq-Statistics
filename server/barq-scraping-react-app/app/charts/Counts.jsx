import { useEffect, useState } from 'react';
import Skeleton from 'react-loading-skeleton'
import 'react-loading-skeleton/dist/skeleton.css'

export default function TotalCount() {
    const [totalCount, setTotalCount] = useState(0);

    useEffect(() => {
        fetch("/api/count", { cache: 'force-cache' })
        .then((res) => res.json())
        .then((data) => {
            setTotalCount(data);
        });
    })

    return (
        <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm w-full">
            <p className="text-sm font-medium text-gray-500 uppercase tracking-wide">Total Count</p>
            {totalCount > 0 ? (
                <p className="text-5xl font-extrabold text-gray-950 tabular-nums mt-2">{totalCount}</p>
            ) : (
                <Skeleton height={50} enableAnimation />
            )}
        </div>
    );
}