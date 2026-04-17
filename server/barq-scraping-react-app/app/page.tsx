'use client'

import dynamic from 'next/dynamic'
import {GenderChart, OrientationChart, RelationshipChart} from "./charts/PieCharts";
import TotalCount from "./charts/Counts";

const Map = dynamic(() => import("./Map"), {ssr: false});

export default function App() {
  return (
    <div className="flex">
      <div className="w-3/4">
        <Map />;
      </div>
      <div className="w-1/4" >
        <h1 className="text-2xl font-medium">
          Hello world!
        </h1>
        
        <div className="flex flex-wrap">
<TotalCount />
        <GenderChart />
          <OrientationChart />
          <RelationshipChart />
        </div>
      </div>
    </div>
  )
}
