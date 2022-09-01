import React from 'react'
import {Radar} from "react-chartjs-2"
import { Chart as  ChartJS } from "chart.js/auto"


export default function RadarChart({chartData, options}) {
  return ( 
    <Radar data={chartData} options={options}/>
  )
}
