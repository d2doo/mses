import React from 'react'

const LandingPage: React.FC = () => {
  const handleKakaoLogin = () => {
    window.location.href = 'http://localhost:8000/api/auth/kakao'
  }

  return (
    <div>
      <h1>소셜 로그인으로 로그인 하기</h1>
      <button onClick={handleKakaoLogin}>카카오로 로그인</button>
    </div>
  )
}

export default LandingPage
