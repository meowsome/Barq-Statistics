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
            Barq is an app for furries to connect with one another based on location. For this project, profile information was collected for a subset of all Barq users. This information was used to perform statistics. Please scroll to the bottom for more information.
          </p>
        
        <div className="flex flex-wrap flex-col space-y-2">
          
          <TotalCount />
          <GenderChart />
          <OrientationChart />
          <RelationshipChart />
          <FursonaChart />
          <HobbiesChart />
          <AgeChart />
          
          <div className="p-3">
            <h3 className="text-2xl font-bold mb-2">About</h3>
            <h5 className="text-xl font-bold">Process</h5>
            <p className="text-body text-gray-600">Technologies used: Android Studio, HTTP Toolkit, Plotly, Pandas, Numpy, Leaflet, Express, React</p>
            <ol className="list-decimal list-inside pl-6 mb-2 text-body text-gray-600">
              <li>Android Studio was used used to run the Barq app on a desktop environment</li>
              <li>HTTP Toolkit was used to sniff packets sent to the Barq API from the Barq app</li>
              <li>The Barq API URLs were analyzed to determine their inputs and outputs</li>
              <li>A set of popular locations in the U.S. and other regions around the world were created</li>
              <li>For each location, Barq profiles were visited and had their data collected starting with the first one until no more could be loaded</li>
              <li>A mini PC was set up with a fresh Barq account to send GET requests using the algorithm described above</li>
              <li>All data was combined and cleaned</li>
            </ol>
            <h5 className="text-lg font-bold">Why?</h5>
            <p className="text-body text-gray-600 mb-2">
              Barq accounts contain information for real furries around the world. Since Barq uses users locations on their mobile devices, generally the data can be considered as accurate. By performing generalized statistics on a subset of this data, unique geographical and other patterns can be observed for real furries.
            </p>
            <h5 className="text-lg font-bold">Ethics</h5>
            <p className="text-body text-gray-600 mb-2">
              All data was collected legally and user profiles are stored anonymously by removing all identifying information after data was collected. No particular user was singled out in these statistics. All data collected is publicly accessible by anyone with the Barq app installed on their device. No private data was compromised. Data was not shared with any other party. No users were solicited in this process. Scraping was performed slowly as to not negatively impact site performance.
            </p>
            <h5 className="text-lg font-bold">Data</h5>
            <p className="text-body text-gray-600 mb-2">
              The data contains a subset of roughly 30% of all Barq users. This is because the data scraped only included users that were active within the past 3 months. There are also areas of the world where scraping was not able to be performed due to limitations. Apologies if your area was not scraped. 
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
