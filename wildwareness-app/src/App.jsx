import './App.css'
import Navbar from './components/Navbar'
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import HomePage from './pages/HomePage'
import About from './pages/About'
import WildfireIncidentsPage from './pages/WildfireIncidentsPage'

function App() {
  return (
    <Router>
        <Navbar/>
        <Routes>
            <Route path="/" element={<HomePage/>}></Route>
            <Route path="/about" element={<About/>}></Route>
            <Route path='/incidents' element={<WildfireIncidentsPage/>}></Route>
        </Routes>
    </Router>
  )
}

export default App
