from abc import ABC, abstractmethod
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.models import EmailAddress
from django.shortcuts import render
from django.contrib.auth import get_user_model

User = get_user_model()

# 소셜 로그인 처리용 추상 클래스
class SocialLoginHandler(ABC):
    @abstractmethod
    def populate_user(self, user, extra_data):
        pass

class KakaoLoginHandler(SocialLoginHandler):
    def populate_user(self, user, extra_data):
        kakao_account = extra_data.get('kakao_account', {})
        profile = kakao_account.get('profile', {})
        user.username = profile.get('nickname', '') or f"user_{extra_data.get('id', '')}"
        user.first_name = kakao_account.get('name', '') or profile.get('nickname', '')


class NaverLoginHandler(SocialLoginHandler):
    def populate_user(self, user, extra_data):
        user.username = extra_data.get('name', '') or extra_data.get('nickname', '') or f"user_{extra_data.get('id', '')}"
        user.first_name = extra_data.get('name', '') or extra_data.get('nickname', '')

# 플랫폼 별 핸들러
class SocialLoginHandlerFactory:
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


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        extra_data = sociallogin.account.extra_data
        provider = sociallogin.account.provider

        handler = SocialLoginHandlerFactory.get_handler(provider)
        handler.populate_user(user, extra_data)
        user.last_name = ''  # 초기화
        return user
    
    def pre_social_login(self, request, sociallogin):
        if sociallogin.is_existing:
            return

        email = sociallogin.account.extra_data.get('email')
        if email:
            try:
                existing_user = EmailAddress.objects.get(email=email).user
                sociallogin.connect(request, existing_user)
            except EmailAddress.DoesNotExist:
                pass
