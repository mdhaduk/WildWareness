import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Navbar from './components/Navbar'
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import HomePage from './pages/HomePage'


function App() {
  const [count, setCount] = useState(0)

  return (
    <Router>
        <Navbar/>
        <Routes>
            <Route path="/" element={<HomePage/>}></Route>
        </Routes>
    </Router>
  )
}

export default App
