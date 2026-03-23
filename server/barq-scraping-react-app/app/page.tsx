'use client'

import React, { useState, useEffect } from "react";
import dynamic from 'next/dynamic'

const Map = dynamic(() => import("./Map"), {ssr: false});

export default function App() {
  return <Map />;
}
