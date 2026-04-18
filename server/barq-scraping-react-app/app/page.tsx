'use client'

import dynamic from 'next/dynamic'
import {GenderChart, OrientationChart, RelationshipChart} from "./charts/PieCharts";
import {AgeChart, FursonaChart} from "./charts/BarCharts";
import TotalCount from "./charts/Counts";

const Map = dynamic(() => import("./Map"), {ssr: false});

export default function App() {
  return (
    <div className="flex">
      <div className="w-2/3 relative">
        <Map />
      </div>
      <div className="w-1/3 p-4 overflow-auto h-screen" >
        <h1 className="text-2xl font-bold mb-2">
          Barq Scraping Statistics
        </h1>
        
        <div className="flex flex-wrap space-y-2">
          <p className="text-body text-gray-600">
            Barq is an app for furries to connect with one another based on location. For this project, profile information was collected for a subset of all Barq users. This information was used to perform analytics and statistics. No individual user was singled out in this project.
          </p>
          <TotalCount />
          <GenderChart />
          <OrientationChart />
          <RelationshipChart />
          <FursonaChart />
          <AgeChart />
        </div>
      </div>
    </div>
  )
}
