import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import LandingPage from './pages/LandingPage'
import KakaoInfoPage from './pages/KaKaoInfoPage'
import Navbar from './components/Navbar'

const App: React.FC = () => {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/userinfo" element={<KakaoInfoPage />} />
      </Routes>
    </Router>
  )
}

export default App
