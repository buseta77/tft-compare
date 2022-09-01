import axios from "axios"
import { useEffect, useState } from "react"
import { Link } from "react-router-dom"
import "./Home.css"

export default function Home() {

    const options = [
        {value: "", text: "--Choose Region--"},
        {value: "br1", text: "Brazil"},
        {value: "eun1", text: "EU (east)"},
        {value: "euw1", text: "EU (West)"},
        {value: "jp1", text: "Japan"},
        {value: "kr", text: "Korea"},
        {value: "la1", text: "Latin America (North)"},
        {value: "la2", text: "Latin America (South)"},
        {value: "na1", text: "North America"},
        {value: "oc1", text: "Ocenia"},
        {value: "tr1", text: "Turkey"},
        {value: "ru", text: "Russia"},
    ]

    const [username, setUsername] = useState("")
    const [username2, setUsername2] = useState("")
    const [region, setRegion] = useState(options[0].value)

    const API_KEY = "RGAPI-c8668e21-898a-41b0-b135-65ccf08590d6" 

    const [user, setUser] = useState(false)
    const [user2, setUser2] = useState([])

    const [userWin, setUserWin] = useState(false)
    const [user2Win, setUser2Win] = useState(false)
    const [usersTie, setUsersTie] = useState(false)

    const [newButton, setNewButton] = useState([])

    const [url, setUrl] = useState("")


    const fetchData = () => {
        const userAPI = "https://" + region + ".api.riotgames.com/tft/summoner/v1/summoners/by-name/" + username + "?api_key=" + API_KEY
        const user2API = "https://" + region + ".api.riotgames.com/tft/summoner/v1/summoners/by-name/" + username2 + "?api_key=" + API_KEY
        const getUser = axios.get(userAPI)
        const getUser2 = axios.get(user2API)
        axios.all([getUser, getUser2]).then(
            axios.spread((...allData) => {
                const allDataUser = allData[0]
                const allDataUser2 = allData[1]

                console.log(allDataUser.data)
                console.log(allDataUser2.data)
                setUser(allDataUser.data)
                setUser2(allDataUser2.data)
            })
        )
    }

    const handleClick = (e) => {
        e.preventDefault()
        fetchData()
    }

    useEffect(() => {
        if (user.summonerLevel > user2.summonerLevel) {
            setUserWin(true)
            setUser2Win(false)
            setUsersTie(false)
            setNewButton(<Link to ="/details"><button className="detail-btn" >Click for Details!</button></Link>)
        } else if (user.summonerLevel < user2.summonerLevel) {
            setUserWin(false)
            setUser2Win(true) 
            setUsersTie(false)
            setNewButton(<Link to ="/details"><button className="detail-btn" >Click for Details!</button></Link>)
        }  else if (user && (user.summonerLevel === user2.summonerLevel)) {
            setUserWin(false)
            setUser2Win(false)
            setUsersTie(true)
            setNewButton(<Link to ="/details"><button className="detail-btn" >Click for Details!</button></Link>)
            console.log(user)
        }
    }, [user])


    return (
            <div className="compare">
                <form>
                    <div className="title">Compare Your Accounts!</div>
                    <div className="players">
                        <div className={`player1 ${userWin ? "win": ""} ${user2Win ? "lose": ""} ${usersTie ? "tie": ""}`} >
                            <label> 
                                <input type="text" placeholder="Username 1" onChange={(e) => {setUsername(e.target.value)}} value={username}/>
                            </label>
                            <h2>Summoner level: {user.summonerLevel}</h2>
                        </div>
                        <div className={`player2 ${userWin ? "lose": ""} ${user2Win ? "win": ""} ${usersTie ? "tie": ""}`}>
                            <label>
                                <input type="text" placeholder="Username 2" onChange={(e) => {setUsername2(e.target.value)}} value={username2}/>
                            </label>
                            <h2>Summoner level: {user2.summonerLevel}</h2>
                        </div>    
                    </div>
                    <div className="compare-bot">
                        <label>
                            <select value={region} onChange={(e) => {setRegion(e.target.value)}}>
                                {options.map(option => (
                                    <option key={option.value} value={option.value}>
                                        {option.text}
                                    </option>
                                ))}    
                            </select>                          
                        </label>
                        <div className="btns">
                        <button className="compare-btn" type="submit" onClick={handleClick}>
                            Compare!
                        </button>
                        {newButton}
                        </div>
                    </div>
                </form>
            </div>
    )
}