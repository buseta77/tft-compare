import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import "./App.css"
import Denemece1 from "./pages/denemeceler/denemece1/Denemece1";
import Denemece2 from "./pages/denemeceler/denemece2/Denemece2";
import Details from "./pages/details/Details";
import Home from "./pages/home/Home"

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route exact path="/" element={<Home/>}/>
          <Route path="/details" element={<Details/>}>
            <Route path="denemece1" element={<Denemece1/>}/>
            <Route path="denemece2" element={<Denemece2/>}/>
          </Route>
        </Routes>
      </Router>
    </div>
  );
}

export default App;
