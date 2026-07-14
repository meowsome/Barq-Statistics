'use client'

import dynamic from 'next/dynamic'
import {GenderChart, OrientationChart, RelationshipChart} from "./charts/PieCharts";
import {AgeChart, FursonaChart, HobbiesChart} from "./charts/BarCharts";
import TotalCount from "./charts/Counts";

const Map = dynamic(() => import("./Map"), {ssr: false});

export default function App() {
  return (
    <div className="flex flex-col sm:flex-row">
      <div className="h-1/2 sm:h-full w-full sm:w-2/3 relative">
        <Map />
      </div>
      <div className="w-full sm:w-1/3 p-4 overflow-auto h-auto md:h-screen" >
        <h1 className="text-3xl font-bold mb-2">
          Barq Scraping Statistics
        </h1>
        
          <p className="text-body text-gray-600 mb-2">
            Barq is an app for furries to connect with one another based on location. For this project, profile information was collected for a subset of all Barq users. This information was used to perform analytics and statistics. No individual user was singled out in this project.
          </p>
        
        <div className="flex flex-wrap flex-col space-y-2">
          
          <TotalCount />
          <GenderChart />
          <OrientationChart />
          <RelationshipChart />
          <FursonaChart />
          <HobbiesChart />
          <AgeChart />
        </div>
      </div>
    </div>
  )
}
