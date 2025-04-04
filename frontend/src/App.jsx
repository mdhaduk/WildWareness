import './App.css'
import Navbar from './components/Navbar'
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import HomePage from './pages/HomePage'
import About from './pages/About'
import Wildfires from './pages/Wildfires'
import WildfireIncidentsPage from './pages/WildfireIncidentsPage';
import Shelters from './pages/Shelters';
import ShelterInstancePage from './pages/ShelterInstancePage';
import NewsReports from './pages/NewsReports'
import NewsReportInstancePage from './pages/NewsReportInstancePage';
import GeneralSearchPage from './pages/GeneralSearchPage';

function App() {
  return (
    <Router>
        <Navbar/>
        <Routes>
            <Route path="/" element={<HomePage/>}></Route>
            <Route path="/about" element={<About/>}></Route>
            <Route path='/search' element={<GeneralSearchPage/>}></Route>
            <Route path='/incidents' element={<Wildfires/>}></Route>
            <Route path='/incidents/:id' element={<WildfireIncidentsPage/>}></Route>
            <Route path='/shelters' element={<Shelters/>}></Route>
            <Route path='/shelters/:id' element={<ShelterInstancePage/>}></Route>
            <Route path='/news' element={<NewsReports/>}></Route>
            <Route path='/news/:id' element={<NewsReportInstancePage/>}></Route>
        </Routes>
    </Router>
  )
}

export default App
