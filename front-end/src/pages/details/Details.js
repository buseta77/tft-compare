import "./Details.css"
import { BrowserRouter, Link, useLocation, Route, Switch, Outlet } from "react-router-dom"
import BarChart from "../../components/BarChart"
import { useState } from "react"

import Denemece1 from "../denemeceler/denemece1/Denemece1"
import Denemece2 from "../denemeceler/denemece2/Denemece2"

export default function Details() { 

    const location = useLocation()
    const stateData = location.state

    const users = stateData["users"]
    const user = stateData["user"]
    const user2 = stateData["user2"]
    


    return (
    <div className="details">
        <nav className="navbar3">
            <ul>
                <li ><Link className="title" to="/">TftBattle</Link> </li>
            </ul>
        </nav>
        <nav className="navbar2">
          <ul>
            <Link to="denemece1" state = {{user: user, users: users, user2: user2}}>Avarege gold</Link>
            <Link to="denemece2" state = {{user: user, users: users, user2: user2}}>Denemece2</Link>
          </ul>
        </nav>
        <div className="detailsMain" >
          <Outlet/>
        </div>
    </div>
    
)
}