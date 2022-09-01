import React, { useState } from 'react'
import { useLocation } from "react-router-dom"
import RadarChart from "../../../components/RadarChart"
import "./Denemece2.css"

export default function Denemece2() {
  const location = useLocation()
  const stateData = location.state

  const users = stateData["users"]
  const user = stateData["user"]
  const user2 = stateData["user2"]

  const [userData, setUserData] = useState({
    labels: ["Africa", "Asia", "Europe", "Latin America", "North America"], 
    datasets: [{
      label: "1950",
      fill: true,
      backgroundColor: "rgba(179,181,198,0.2)",
      borderColor: "rgba(179,181,198,1)",
      pointBorderColor: "#fff",
      pointBackgroundColor: "rgba(179,181,198,1)",
      data: [8.77,55.61,21.69,6.62,6.82]
    }, {
      label: "2050",
      fill: true,
      backgroundColor: "rgba(255,99,132,0.2)",
      borderColor: "rgba(255,99,132,1)",
      pointBorderColor: "#fff",
      pointBackgroundColor: "rgba(255,99,132,1)",
      pointBorderColor: "#fff",
      data: [25.48,54.16,7.61,8.06,4.45]
    }]
  })

  const [options, setOptions] = useState({
    title: {
      display: true,
      text: 'Distribution in % of world population'
    }
  })
  return (
    <div className='graphs'>
      <div className='chart'>
        <RadarChart chartData={userData} options={options}/>
      </div>
    </div>
  )
}
