'use client'

import React, { useState, useEffect } from "react";
import dynamic from 'next/dynamic'

const Map = dynamic(() => import("./Map"), {ssr: false});
// const GenderChart = dynamic(() => import("./charts/GenderChart"), {ssr: false});
import GenderChart from "./charts/GenderChart";

// TODO implement suspense

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
        
        <GenderChart />
      </div>
    </div>
  )
}
