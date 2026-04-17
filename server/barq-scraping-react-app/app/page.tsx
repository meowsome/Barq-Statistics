'use client'

import dynamic from 'next/dynamic'
import {GenderChart, OrientationChart, RelationshipChart} from "./charts/PieCharts";
import {FursonaChart} from "./charts/BarCharts";
import TotalCount from "./charts/Counts";

const Map = dynamic(() => import("./Map"), {ssr: false});

export default function App() {
  return (
    <div className="flex">
      <div className="w-2/3">
        <Map />
      </div>
      <div className="w-1/3 p-4 overflow-auto h-screen" >
        <h1 className="text-2xl font-medium">
          Hello world!
        </h1>
        
        <div className="flex flex-wrap">
          <TotalCount />
          <GenderChart />
          <OrientationChart />
          <RelationshipChart />
          <FursonaChart />
        </div>
      </div>
    </div>
  )
}
