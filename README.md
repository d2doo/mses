# **MSES SERVICE**

이 프로젝트는 Django를 기반으로 일반 회원가입 및 소셜 로그인을 구현한 웹 애플리케이션입니다.

---

## **목차**

1. 프로젝트 소개 
2. 설치 및 실행 방법   
3. 주요 코드 설명 
4. 프로세스 흐름 
5. 참고 자료 

---

## **프로젝트 소개**

MSES SERVICE는 **일반 회원가입 및 로그인**과 **OAuth2.0 기반 소셜 로그인**(카카오, 네이버)을 제공합니다  

### **핵심 기능**
1. **일반 회원가입 및 로그인**  
   - 사용자 정의 모델과 Django 인증 시스템을 사용한 회원가입 및 로그인

2. **OAuth2.0 기반 소셜 회원가입 및 로그인**  
   - 카카오, 네이버 소셜 로그인 제공  

### **부가 기능**
1. **로그아웃**  
   - 로그인된 사용자의 세션을 종료하고 `/users/landing`으로 리다이렉트

2. **이메일 중복 처리**  
   - 동일 이메일이 여러 계정에서 사용될 경우 계정을 하나로 묶어 관리  
   - **예시**:  
     - 카카오 계정의 이메일과 네이버 계정의 이메일이 같으면, 먼저 생성된 계정으로 로그인 처리  
     - 일반 회원가입 시, 이미 동일한 이메일로 등록된 소셜 계정이 있으면 회원가입 불가

3. **접근 권한 관리**  
   - 로그인 상태에 따라 특정 URL 접근을 제한.  
   - **예시**:  
     - 로그아웃 상태에서 `/users/userinfo` 접근 불가 → `/users/landing`으로 리다이렉트.  
     - 로그인 상태에서 `/users/landing` 접근 불가 → `/users/userinfo`로 리다이렉트.  

---

## 설치 및 실행 방법

> Visual Studio Code(VSCode)의 터미널을 기준으로 작성하였습니다.

1. **레포지토리 클론:**
   ```bash
   git clone https://github.com/d2doo/mses.git
   cd be/
   ```

2. **가상환경 설정 및 의존성 설치:**
   - **가상환경 생성:**  
     ```bash
     python -m venv venv
     ```
   - **가상환경 활성화:**  
     - **Windows:**  
       ```bash
       source venv\Scripts\activate
       ```
   - **의존성 설치:**  
     ```bash
     pip install -r requirements.txt
     ```

3. **환경 변수 설정:**
   - **`.env` 파일 위치:** 프로젝트 루트 디렉토리(예: `manage.py`와 동일한 위치)에 `.env` 파일 생성
   - `.env` 파일은 보안 상 이메일에 첨부하였습니다.

4. **데이터베이스 마이그레이션:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **서버 실행:**
   ```bash
   python manage.py runserver
   ```

---


## **주요 코드 설명**

### **프로젝트 개요**

Django의 **allauth** 패키지와 Django 기본 **auth** 시스템을 활용하여 일반 회원가입 및 OAuth2.0 기반 소셜 로그인을 구현했습니다.  
- **일반 회원가입**: 사용자 정의 모델(`User`)을 사용하여 사용자 데이터를 저장.  
- **소셜 로그인**: `django-allauth`를 사용하여 OAuth2.0 기반 로그인(Kakao, Naver)을 처리.  
- 일반 회원가입과 소셜 로그인은 독립적으로 관리되며, 동일 이메일 사용 시 계정을 통합 관리하도록 설계.  

---

### **`models.py`**

`User` 모델은 Django의 기본 사용자 모델을 확장한 **커스텀 사용자 모델**입니다.  
소셜 로그인에서 제공하는 데이터(이메일, 닉네임)를 저장할 수 있도록 필드를 확장하였습니다.  

#### 코드:
```python
from django.contrib.auth.models import AbstractUser
from django.db import models

# User 커스텀
class User(AbstractUser):
    email = models.EmailField(unique=True)  # 이메일 (unique 설정)
    nickname = models.CharField(max_length=50, blank=True)  # 닉네임 (선택 필드)

    def __str__(self):
        return self.username
```

---

### **`views.py`**

#### **회원가입 처리**
- 일반 회원가입 요청을 처리하는 **`signup_view`** 함수는 Django 기본 폼 시스템을 사용해 구현되었습니다.  
- 유효한 데이터를 입력받으면 새 사용자 계정을 생성하고 자동으로 로그인합니다.
- `django.shortcuts`의 `render()`메서드를 활용하여 http 요청과 응답을 처리하였습니다.

#### 코드:
```python
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, get_backends
from .forms import SignupForm

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        # 유효성 검증
        if form.is_valid():
            user = form.save() # 유효한 폼 데이터로 사용자 저장
            backend = get_backends()[0] # 인증 백엔드 가져오기
            auth_login(request, user, backend=backend.__module__ + '.' + backend.__class__.__name__) # 백엔드 설정으로 로그인
            return redirect('/users/userinfo/') # 사용자 정보 페이지로 redirect
    else:
        form = SignupForm() # GET 요청시 비어있는 폼 제
    context = {
        'form': form
    }
    return render(request, 'signup.html', context)
```

---

### **OAuth2.0 소셜 로그인 처리**

Django `allauth` 패키지를 활용하여 Kakao 및 Naver OAuth2.0 회원가입과 로그인을 구현하였습니다.  
- 소셜 로그인은 **allauth**의 `SocialAccount` 모델에서 관리되며, 일반 회원가입 데이터(`User` 모델)와 독립적으로 저장됩니다.  
- `pre_social_login` 및 `populate_user` 메서드를 커스터마이징하여 데이터 통합 및 사용자 생성 방식을 제어합니다.

#### **핵심 코드**
- **사용자 모델 매핑 및 생성**

### **`adapters.py`**

Django `allauth`의 기본 소셜 계정 어댑터(DefaultSocialAccountAdapter)를 커스터마이징하여 **Kakao** 및 **Naver** OAuth2.0 로그인을 처리하였습니다.  

1. **소셜 로그인 데이터 처리**:  
   - 각 제공자(Kakao, Naver)의 데이터를 `populate_user` 메서드에서 가공하여 사용자 모델에 매핑.
   - 추상 클래스와 팩토리 패턴을 활용해 제공자별 데이터 처리 로직을 분리.

2. **중복 이메일 처리**:  
   - `pre_social_login` 메서드에서 중복된 이메일을 가진 계정을 연결.

---

#### 코드:
```python
from abc import ABC, abstractmethod
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.models import EmailAddress
from django.shortcuts import render
from django.contrib.auth import get_user_model

User = get_user_model()

# 소셜 로그인 데이터 처리하는 추상클래스
class SocialLoginHandler(ABC):
    @abstractmethod
    def populate_user(self, user, extra_data):
        pass

# 카카오 데이터 처리
class KakaoLoginHandler(SocialLoginHandler):
    def populate_user(self, user, extra_data):
        kakao_account = extra_data.get('kakao_account', {})
        profile = kakao_account.get('profile', {})
        user.username = profile.get('nickname', '') or f"user_{extra_data.get('id', '')}"
        user.first_name = kakao_account.get('name', '') or profile.get('nickname', '')

# 네이버 데이터 처리
class NaverLoginHandler(SocialLoginHandler):
    def populate_user(self, user, extra_data):
        user.username = extra_data.get('name', '') or extra_data.get('nickname', '') or f"user_{extra_data.get('id', '')}"
        user.first_name = extra_data.get('name', '') or extra_data.get('nickname', '')

# 팩토리 클래스
class SocialLoginHandlerFactory:
    # 제공자 별 핸들러
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

# django allauth 소셜 계정 어댑터 커스텀
class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    # 로그인 데이터를 사용자 모델에 매핑
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        extra_data = sociallogin.account.extra_data
        provider = sociallogin.account.provider

        # 제공자 별 데이터 처리
        handler = SocialLoginHandlerFactory.get_handler(provider)
        handler.populate_user(user, extra_data)
        user.last_name = ''  # 초기화
        return user

    # 중복 이메일 계정 통합 처리
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
```

---

#### **주요 로직 설명**

1. **`populate_user`**:
   - 소셜 제공자로부터 받은 데이터를 사용자 모델에 매핑.
   - 확장성을 위해 Kakao와 Naver 데이터를 분리 처리.

2. **`pre_social_login`**:
   - 중복 이메일 확인 및 기존 사용자 계정 연결.
   - `EmailAddress` 모델을 활용해 이메일 중복 여부를 확인.

3. **추상 클래스 및 팩토리 패턴**:
   - `SocialLoginHandler` 추상 클래스를 통해 공통 인터페이스 정의.
   - 팩토리 클래스(`SocialLoginHandlerFactory`)를 활용해 제공자별 로직을 분리.

---

### **부가기능 설명**

#### **로그아웃**
Django 기본 `auth` 시스템의 `logout()` 메서드를 사용하여 구현.

```
from django.urls import path
from django.contrib.auth.views import LogoutView

urlpatterns = [
    ...
    path('logout/', LogoutView.as_view(), name='logout'),
]
```

#### **URL 접근 제한**
- 로그인 상태를 기반으로 특정 페이지 접근 제한.  
  - 예: 로그인 상태에서 `/users/landing` 접근 시 리다이렉트.  
  - 로그아웃 상태에서 `/users/userinfo` 접근 시 리다이렉트.

```
from django.shortcuts import render, redirect
from allauth.socialaccount.models import SocialAccount

def landing_view(request):
    # 로그인 상태인지 확인 후 리다이렉트
    if request.user.is_authenticated:
        return redirect('/users/userinfo')
    
    return render(request, 'landing.html')

def userinfo_view(request):
    # 로그인 상태인지 확인 후 리다이렉트
    if not request.user.is_authenticated:
        return redirect('/users/landing')
    
    social_account = SocialAccount.objects.filter(user=request.user).first()
    extra_data = social_account.extra_data if social_account else {}
    context = {
        'extra_data': extra_data
    }
    return render(request, 'userinfo.html', context)
```

---


## 프로세스 흐름

### 1. **회원가입 및 로그인**

#### **일반 회원가입**
1. **`GET` 요청**:
   - 클라이언트가 `/users/signup` 경로로 접근
   - Django는 빈 회원가입 폼을 렌더링하여 사용자에게 제공

2. **`POST` 요청**:
   - 사용자가 입력한 데이터를 서버로 전송
   - Django는 전달된 데이터의 유효성을 검증
     - 유효성 검증 실패 시: 오류 메시지와 함께 폼 재전송
     - 유효성 검증 성공 시: 새 사용자 계정을 생성
   - 계정 생성 후:
     - 사용자 자동 로그인 처리
     - 사용자 정보 페이지(`/users/userinfo/`)로 리다이렉트

#### **소셜 로그인 (OAuth2.0)**
1. **소셜 로그인 요청**:
   - 사용자가 카카오/네이버 로그인 버튼 클릭
   - 해당 소셜 플랫폼의 인증 페이지로 리다이렉트

2. **OAuth2.0 인증**:
   - 사용자가 소셜 플랫폼에서 인증 승인
   - 인증이 완료되면, Django `allauth`가 인증 코드를 받아 콜백 URL로 처리

3. **사용자 데이터 처리**:
   - Django `allauth`가 소셜 플랫폼에서 사용자 정보를 가져옴
   - 가져온 데이터를 기반으로 `populate_user` 메서드가 실행:
     - 사용자의 닉네임, 프로필 이미지, 이메일 등 저장
     - 기존 동일 이메일의 계정이 존재할 경우
       - 계정 연결
       - 로그인 후 사용자 정보 페이지(`/users/userinfo/`)로 리다이렉트

---

### 2. **사용자 정보 접근**

#### **로그인 상태에 따른 URL 접근 제한**
1. **로그아웃 상태**:
   - `/users/userinfo/` 접근 시 로그인 페이지(`/users/landing/`)로 리다이렉트

2. **로그인 상태**:
   - `/users/landing/` 접근 시 사용자 정보 페이지(`/users/userinfo/`)로 리다이렉트
   - 이미 로그인된 상태에서 불필요한 회원가입/로그인 페이지 표시 방지

---

### 3. **이메일 중복 처리**

#### **소셜 로그인과 일반 회원가입 간 이메일 중복**
1. **시나리오 1**: 
   - 카카오 계정과 네이버 계정의 이메일이 동일한 경우
   - 동일 이메일을 사용하는 다른 소셜 계정 로그인 시, 기존 계정과 연결

2. **시나리오 2**:
   - 동일 이메일로 일반 회원가입 시도
   - 이미 사용 중인 이메일로는 일반 회원가입 불가

---

### 4. **전체 흐름 요약**

1. **회원가입/로그인 요청 → 데이터 검증 → 계정 생성/로그인 → 리다이렉트**
2. **OAuth2.0 → 인증 및 사용자 정보 처리 → 기존 계정과 연결/새 계정 생성**
3. **로그인 상태 → URL 접근 제한 및 보호**

---

---

## 참고 자료

- [Django 공식 문서](https://docs.djangoproject.com/)
- [django-allauth GitHub](https://github.com/pennersr/django-allauth)
- [카카오 OAuth API](https://developers.kakao.com/)
- [네이버 OAuth API](https://developers.naver.com/)

---

읽어주셔서 감사합니다 😄
```
