from abc import ABC, abstractmethod

class SocialLoginHandler(ABC):
    """
    소셜 로그인 데이터를 처리하는 추상 클래스
    각 소셜 제공자는 이 클래스를 상속받아 커스터마이징함
    """
    @abstractmethod
    def populate_user(self, user, extra_data):
        pass


class KakaoLoginHandler(SocialLoginHandler):
    """
    카카오 데이터 처리
    """
    def populate_user(self, user, extra_data):
        kakao_account = extra_data.get('kakao_account', {})
        profile = kakao_account.get('profile', {})
        user.username = profile.get('nickname', '') or f"user_{extra_data.get('id', '')}"
        user.first_name = kakao_account.get('name', '') or profile.get('nickname', '')


class NaverLoginHandler(SocialLoginHandler):
    """
    네이버 데이터 처리.
    """
    def populate_user(self, user, extra_data):
        user.username = extra_data.get('name', '') or extra_data.get('nickname', '') or f"user_{extra_data.get('id', '')}"
        user.first_name = extra_data.get('name', '') or extra_data.get('nickname', '')


class SocialLoginHandlerFactory:
    """
    플랫폼별 핸들러 생성(팩토리)
    """
    HANDLERS = {
        'kakao': KakaoLoginHandler,
        'naver': NaverLoginHandler,
    }

    @staticmethod
    def get_handler(provider):
        handler_class = SocialLoginHandlerFactory.HANDLERS.get(provider)
        if handler_class is None:
            raise ValueError(f"Provider '{provider}'에 대한 핸들러가 정의되지 않았습니다.")
        return handler_class()


# MySocialAccountAdapter 수정
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        extra_data = sociallogin.account.extra_data
        provider = sociallogin.account.provider

        # 팩토리에서 적절한 핸들러 가져오기
        handler = SocialLoginHandlerFactory.get_handler(provider)
        handler.populate_user(user, extra_data)

        user.last_name = ''  # 성이 없는 경우 빈 문자열로 설정
        return user
