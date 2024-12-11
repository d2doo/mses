import React from 'react'
import { useLocation } from 'react-router-dom'

type UserInfo = {
  id: string
  name: string
  email: string
  nickname?: string
  birthday?: string
  profileImage?: string
}

const KakaoInfoPage: React.FC = () => {
  const location = useLocation()

  const queryParams = new URLSearchParams(location.search)
  const userInfo: UserInfo = {
    id: queryParams.get('id') || 'Unknown',
    name: queryParams.get('name') || 'Unknown',
    email: queryParams.get('email') || 'Unknown',
    nickname: queryParams.get('nickname') ?? undefined,
    birthday: queryParams.get('birthday') ?? undefined,
    profileImage: queryParams.get('profile_image_url') ?? undefined,
  }

  return (
    <div>
      <h1>카카오 사용자 정보</h1>
      <p>
        <strong>아이디:</strong> {userInfo.id}
      </p>
      <p>
        <strong>이름:</strong> {userInfo.name}
      </p>
      <p>
        <strong>이메일:</strong> {userInfo.email}
      </p>

      {/* 선택 동의 항목 */}
      {userInfo.nickname && (
        <p>
          <strong>닉네임:</strong> {userInfo.nickname}
        </p>
      )}

      {userInfo.birthday && (
        <p>
          <strong>생일:</strong> {userInfo.birthday}
        </p>
      )}

      {userInfo.profileImage && (
        <div>
          <strong>프로필 사진:</strong>
          <img
            src={userInfo.profileImage}
            alt="Profile"
            style={{ width: '100px', borderRadius: '50%' }}
          />
        </div>
      )}

      {!userInfo.nickname && !userInfo.birthday && !userInfo.profileImage && (
        <p>선택 동의 항목 정보가 없습니다.</p>
      )}
    </div>
  )
}

export default KakaoInfoPage
