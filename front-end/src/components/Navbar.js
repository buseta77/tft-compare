import { Link } from "react-router-dom"

import "./Navbar.css"

export default function Navbar() {
    return (
        <nav className="navbar">
            <ul>
                <li ><Link className="title" to="/">TftBattle</Link> </li>
            </ul>
        </nav>
    )
}

