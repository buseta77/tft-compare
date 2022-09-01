import React, { useState } from 'react'
import {useLocation} from "react-router-dom"
import BarChart from "../../../components/BarChart"

export default function Denemece1() {
    const location = useLocation()
    const stateData = location.state

    const users = stateData["users"]
    const user = stateData["user"]
    const user2 = stateData["user2"]
    console.log(users)
    console.log(Object.keys(user.top_items[0]))
    const [userData, setUserData] = useState({
        labels: [user.top_items[0].name, user.top_items[1].name, user.top_items[2].name], 
        datasets: [{
          label: "Most used items", 
          backgroundColor: ["blue", "red", "green"],
          data: [user.top_items[0].count, user.top_items[1].count, user.top_items[2].count]
        }]
      })
  
      const [options, setOptions] = useState({
        options: {
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      })

      const [userData2, setUserData2] = useState({
        labels: [user2.top_items[0].name, user2.top_items[1].name, user2.top_items[2].name], 
        datasets: [{
          label: "Most used items", 
          backgroundColor: ["blue", "red", "green"],
          data: [user2.top_items[0].count, user2.top_items[1].count, user2.top_items[2].count]
        }]
      })
  
      const [options2, setOptions2] = useState({
        options: {
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      })


  return (
    <div className='graphs'>
         <div className="chart">
            <h1>{user.username}</h1>
          <BarChart chartData={userData} options={options}/>
        </div>
        <div className="chart">
        <h1>{user2.username}</h1>
          <BarChart chartData={userData2} options={options2}/>
        </div>
    </div>
  )
}
