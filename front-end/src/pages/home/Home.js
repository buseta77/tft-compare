import axios from "axios"
import { useEffect, useState } from "react"
import { Link } from "react-router-dom"
import {useSound} from "use-sound"
import "./Home.css"

import doorSound from "../../logo/sound.wav"
import metalLoading from "../../logo/metal-loading.mp3"
import toggle from "../../logo/toggle.mp3"
import choose from "../../logo/choose.mp3"
import compare from "../../logo/compare.mp3"

export default function Home() {

    const options = [
        {value: "", text: "--Choose Region--"},
        {value: "br1", text: "Brazil"},
        {value: "eun1", text: "EU (East)"},
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

    const [user, setUser] = useState(false)
    const [user2, setUser2] = useState([])
    const [users, setUsers] = useState([])

    const [userWin, setUserWin] = useState(false)
    const [user2Win, setUser2Win] = useState(false)
    const [usersTie, setUsersTie] = useState(false)
    const [usernameLeft, setUsernameLeft] = useState([])
    const [usernameRight, setUsernameRight] = useState([])
    const [left, setLeft] = useState(false)
    const [right, setRight] = useState(false)
    const [map, setMap] = useState(false)
    
    const [pp, setPp] = useState([])
    const [league, setLeague] = useState([])
    const [wins, setWins] = useState([])
    const [loses, setLoses] = useState([])
    const [pp2, setPp2] = useState([])
    const [league2, setLeague2] = useState([])
    const [wins2, setWins2] = useState([])
    const [loses2, setLoses2] = useState([])
    const [avg, setAvg] = useState([])
    const [playedTogether, setPlayedTogether] = useState([])
    const [topFour, setTopFour] = useState([])
    const [first, setFirst] = useState([])
    const [last, setLast] = useState([])
    const [avg2, setAvg2] = useState([])
    const [topFour2, setTopFour2] = useState([])
    const [first2, setFirst2] = useState([])
    const [last2, setLast2] = useState([])

    const [errorCheck, setErrorCheck] = useState([])
    const [errorCheckToggle, setErrorCheckToggle] = useState([])
    const [isErrorCheck, setİsErrorCheck] = useState(false)
    const [yellow, setYellow] = useState(false)

    const [disableButton, setDisableButton] = useState(false)
    const [changeButton, setChangeButton] = useState(true)
    const [loadingButton, setLoadingButton] = useState(false)

    const[buttonText, setButtonText] = useState()

    const [text, setText] = useState("")
    const [textCheck, setTextCheck] = useState(false)

    const [disableInputs, setDisableInputs] = useState(false)

    const [userMode, setUserMode] = useState(false)
    const [mapMode, setMapMode] = useState("")

    const [sound, setSound] = useState(true)

    const [volume, setVolume] = useState(0.20)
    const [play] = useSound(doorSound, {volume})
    const [metalLoad, {stop}] = useSound(metalLoading, {volume})
    const [toggleMode] = useSound(toggle, {volume})
    const [regionSound] = useSound(choose, {volume})
    const [compareSound] = useSound(compare, {volume})

    const fetchData = async (e) => {
        try {
            sound && compareSound()
            sound && metalLoad()
            setDisableButton(true)
            setLoadingButton(true)
            setTextCheck(true)
            setDisableInputs(true)
            const response = await axios.post("api/compare/", {
            // https://tft-comparing.herokuapp.com
            // C9 k3soju    becca tilts
            username1: username, 
            username2: username2,
            server: region
            })
            console.log(response.data.user1)
            console.log(response.data.user2)
            console.log(response.data)
            setUser(response.data.user1)
            setUser2(response.data.user2)
            setUsers(response.data)
            setDisableButton(false)
            sound && stop()
            setLoadingButton(false)
            setTextCheck(true)
            setDisableInputs(false)
        } catch (error) {
            setErrorCheck(error.response.status)
            setErrorCheckToggle(error.response.status)
            console.log(error)
            sound && stop()
            setDisableButton(false)
            setLoadingButton(false)
            setTextCheck(false)
            setDisableInputs(false)
    }}

    useEffect(() => {
        if (region !== "") {
            setMap(true)
        } else if (region === "") {
            setMap(false)
        }
        sound && regionSound()
    }, [region])

    useEffect(() => {
        if (region !== "" && username !== "" && username2 !== "") {
            setDisableButton(false)
        } else if (region === "" || username === "" || username2 === ""){
            setDisableButton(true)
        }
    }, [region, username, username2])


    useEffect(() => {
        if (isErrorCheck === false && textCheck === true && region !== "" && username !== "" && username2 !== "") {
            setText("")
        }else if (region === "" && username === "" && username2 === "") {
            setText("Select region and enter summoner names.")
            setYellow(true)
        } else if (isErrorCheck === true && textCheck === false && errorCheck === 400) {
            setText("Summoner name 1 is not valid.")
            setYellow(false)
        } else if (isErrorCheck === true && textCheck === false && errorCheck === 405) {
            setText("Summoner name 2 is not valid.")
            setYellow(false)
        }else if (isErrorCheck === true && textCheck === false && errorCheck === 404) {
            setText("Players have not played together in their last 200 games.")
            setYellow(false)
        }else if (isErrorCheck === true && textCheck === false && errorCheck === 500) {
            setText("Server is down.")
            setYellow(false)
        }else if ((isErrorCheck === true && textCheck === true && (region !== "" && username !== "" && username2 !== ""))){
            setText("Based on the matches played between the two players in their last 200 games")
            setYellow(false)
        }
    }, [region, username, username2, errorCheckToggle, user])

    useEffect(() => {
        if (user === false && loadingButton === true) {
            setButtonText("Loading...")
        }else if (user === false) {
            setButtonText("Compare!")
        } else if (loadingButton === false) {
            setButtonText("Click for Detailed Statistics")
        }
    }, [user, loadingButton])

    useEffect(() => {
        if (user && user2) {
        if (user.avg < user2.avg) {
            setUserWin(true)
            setUser2Win(false)
            setUsersTie(false)
        } else if (user.avg > user2.avg) {
            setUserWin(false)
            setUser2Win(true) 
            setUsersTie(false)
        }  else if (user && (user.avg === user2.avg)) {
            setUserWin(false)
            setUser2Win(false)
            setUsersTie(true)
        }
        user && setUsernameLeft(<h1>{username}</h1>)
        user && setUsernameRight(<h1>{username2}</h1>)
        user && setLeft(!left)
        user && setRight(!right)
        user && sound && play()
        setİsErrorCheck(false)

    }}, [user])

    useEffect(() =>{
        if (user && user2 && user) {
        setPp(user.pp)
        setLeague(user.league)
        setWins(user.total_wins)
        setLoses(user.total_losses)
        setPp2(user2.pp)
        setLeague2(user2.league)
        setWins2(user2.total_wins)
        setLoses2(user2.total_losses)
        setAvg(user.avg)
        setPlayedTogether(users.played_together)
        setTopFour(user.top4)
        setFirst(user.first)
        setLast(user.eight)
        setAvg2(user2.avg)
        setTopFour2(user2.top4)
        setFirst2(user2.first)
        setLast2(user2.eight)
    }
    }, [user2])

    useEffect(() =>{
        if (errorCheck && errorCheck !== "" ) {
            setİsErrorCheck(true)
            setErrorCheckToggle()
            setChangeButton(true)
        }
    }, [errorCheckToggle])
    
    const handleClick = (e) => {
        setChangeButton(!changeButton)
        if (changeButton) {
            e.preventDefault()
            fetchData()
        } 
    }

    const handleAgain = (e) => {
        e.preventDefault()
        setUser(false)
        setLeft(!left)
        setRight(!right)
        sound && play()
        setChangeButton(!changeButton)
        setTimeout(() => {
            setPp()
            setLeague()
            setWins()
            setLoses()
            setPp2()
            setLeague2()
            setWins2()
            setLoses2()
            setAvg()
            setTopFour()
            setFirst()
            setLast()
            setAvg2()
            setTopFour2()
            setFirst2()
            setLast2()
        }, 3200)
    }
    
    const modeHandler = (e) => {
        setUserMode(!userMode)
        sound && toggleMode()
    }

    useEffect(() => {
        if (userMode) {
            setMapMode("r")
        } else if (!userMode) {
            setMapMode("")
        }
    }, [userMode])

    const soundHandler = () => {
        setSound(!sound)
    }       

    return (
        <div className= {`${userMode ? "blue-bg": "black-bg"}`}>
        <div className="main-container" style={{ 
            width: "100%",
            height: "100vh",
            display: "flex",
            flexDirection: "column",
            backgroundImage: `url(/${map ? region + mapMode: "world" + mapMode}.png)`,
            backgroundPosition: "center",
            backgroundSize: 'cover',
            backgroundRepeat: 'no-repeat'
        }}>
            <nav className="navbar">
            <ul>
                <li ><Link className="title" to="/">TftBattle</Link> </li>
                <label className="toggle">
                    <input className="toggle-checkbox" type="checkbox" onClick={modeHandler}></input>
                    <div className="toggle-switch"></div>
                    <span className="toggle-label">Mode</span>
                </label>
                <label className="toggle2">
                    <input className="toggle-checkbox" type="checkbox" onClick={soundHandler}></input>
                    <div className="toggle-switch2"></div>
                    <span className="toggle-label">Sound</span>
                </label>
            </ul>
            </nav>
            <div className="main">
                    <div className={`main1 ${user ? "main1-3-opa": "main1-3-opa2"}`}>
                        <h2>{usernameLeft}</h2>
                        <img src={pp} alt="" />
                        <h3>League: {league}</h3>
                        <h3>Total Wins: {wins}</h3>
                       <h3>Total Loses: {loses}</h3>
                    </div>
                    <div className="main2">
                        <div className="header">
                            {!user && <select value={region} onChange={(e) => {setRegion(e.target.value)}} disabled={disableInputs}>
                                {options.map(option => (
                                    <option key={option.value} value={option.value}>
                                        {option.text}
                                    </option>
                                ))}  
                            </select>}
                            {user && <button className="compare-again-btn" onClick={handleAgain}>Click to Compare Again!</button>}
                        </div>
                        <div className="middle">
                        <div className="back-main">
                            <div className={`user-back ${userWin ? "win": ""} ${user2Win ? "lose": ""} ${usersTie ? "tie": ""}`}>
                                <div className="users-data">
                                    {<h2>Avarage : </h2>}
                                    {<h2>Top Four : </h2>}
                                    {<h2>First Place : </h2>}
                                    {<h2>Last Place : </h2>}
                                    {<h2>Total Games : </h2>}
                                </div>
                                <div className="span">
                                    <h2>{avg}</h2>
                                    <h2>{topFour}</h2>
                                    <h2>{first}</h2>
                                    <h2>{last}</h2>
                                    <h2>{playedTogether}</h2>
                                </div>
                            </div>
                            <div className={`user2-back ${userWin ? "lose": ""} ${user2Win ? "win": ""} ${usersTie ? "tie": ""}` }>
                            <div className="users-data">
                                    {<h2>Avarage : </h2>}
                                    {<h2>Top Four : </h2>}
                                    {<h2>First Place : </h2>}
                                    {<h2>Last Place : </h2>}
                                    {<h2>Total Games : </h2>}
                                </div>
                                <div className="span">
                                    <h2>{avg2}</h2>
                                    <h2>{topFour2}</h2>
                                    <h2>{first2}</h2>
                                    <h2>{last2}</h2>
                                    <h2>{playedTogether}</h2>
                                </div>
                            </div>
                        </div>
                        <div className={`${userMode ? "front-main-mode": "front-main"}`}>
                            <div className={`${userMode ? "user-front-mode": "user-front"} ${left ? "left": ""}`} >
                                <div className="input-container" >
                                    <input type="text" placeholder="Summoner Name 1" onChange={(e) => {setUsername(e.target.value)}} value={username} disabled={disableInputs}/>
                                </div>
                            </div>
                            <div className={`${userMode ? "user2-front-mode": "user2-front"} ${right ? "right": ""}`}>
                                <div className="input-container2">
                                    <input type="text" placeholder="Summoner Name 2" onChange={(e) => {setUsername2(e.target.value)}} value={username2} disabled={disableInputs}/>
                                </div>
                            </div>
                        </div>
                        </div>
                        <div className="errors">
                            <div className={`${isErrorCheck ? "error-bg-red" : "error-bg"} ${yellow ? "error-bg-yellow" : ""}`}>
                                {/* <h4>{`${isErrorCheck ? "At least one user not found. Please check usernames and server name." : "Based on the matches played between the two summoners in their last 200 games"} `}</h4> */}
                                <h4>{text}</h4>
                            </div> 
                        </div>
                        <div className="bottom">
                            <Link to ={{pathname:`${!user ? "/" : "details"}`}}><button className={`${!user ? "compare-btn" : "detail-btn"} ${disableButton ? "disable-btn" : ""}`} type="submit" onClick={handleClick} disabled={disableButton}>{buttonText}</button></Link>
                            <Link to ="/details" state = {{user: user, users: users, user2: user2}} >Details</Link>
                        </div>
                    </div>
                    <div className={`main3 ${user ? "main1-3-opa": "main1-3-opa2"}`}>
                        <h2>{usernameRight}</h2>
                        <img src={pp2} alt="" />
                        <h3>League: {league2}</h3>
                        <h3>Total Wins: {wins2}</h3>
                       <h3>Total Loses: {loses2}</h3>
                    </div>
            </div>
        </div>
        </div>
    )
}