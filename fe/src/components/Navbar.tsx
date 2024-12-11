import React from 'react'
import { Link } from 'react-router-dom'

const Navbar: React.FC = () => {
  return (
    <nav>
      <ul>
        <li>
          <Link to="/">메인</Link>
        </li>
        <li>
          <Link to="/userinfo">내 정보</Link>
        </li>
      </ul>
    </nav>
  )
}

export default Navbar
