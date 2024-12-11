from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.models import EmailAddress

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        동일한 이메일을 가진 기존 사용자가 있을 경우 소셜 계정을 연결
        """
        # 이미 연결된 계정인 경우 그대로 진행
        if sociallogin.is_existing:
            return

        # 소셜 로그인 데이터에서 이메일 가져오기
        email = sociallogin.account.extra_data.get('email')
        if email:
            try:
                # 동일한 이메일을 가진 기존 사용자 계정 찾기
                existing_user = EmailAddress.objects.get(email=email).user

                # 소셜 계정을 기존 사용자 계정에 연결
                sociallogin.connect(request, existing_user)
            except EmailAddress.DoesNotExist:
                pass  # 기존 계정이 없으면 새 계정 생성
    
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        extra_data = sociallogin.account.extra_data
        provider = sociallogin.account.provider

        print("DEBUG: sociallogin.account.extra_data", extra_data)

        if provider == "kakao":
            # 카카오 데이터 처리
            kakao_account = extra_data.get('kakao_account', {})
            profile = kakao_account.get('profile', {})
            user.username = profile.get('nickname', '') or f"user_{sociallogin.account.uid}"
            user.first_name = kakao_account.get('name', '') or profile.get('nickname', '')
        elif provider == "naver":
            # 네이버 데이터 처리
            user.username = extra_data.get('name', '') or extra_data.get('nickname', '') or f"user_{sociallogin.account.uid}"
            user.first_name = extra_data.get('name', '') or extra_data.get('nickname', '')

        user.last_name = ''  # 성이 없는 경우 빈 문자열로 설정

        print("DEBUG: Populated user:", user.username, user.first_name)
        return user