# B-12_group_quarrel   
1. toml 파일을 install 해주세요.   
2. 패키지는 아래와 같이 설치되어 있습니다.   
{   
  python = "^3.11"   
  django = "^4.2"   
  djangorestframework-simplejwt = "^5.2.2"   
  django-cors-headers = "^3.14.0"   
  djangorestframework = "^3.14.0"   
}   
   
3. users app 은 기본적으로 필요한 것이라 임의로 생성해 놓았습니다. (urls설정을 미리 해 두었습니다 확인해 주세요!)   
4. settings의 설정에서 secret_key는 json으로 설정을 해놓았습니다.   
4_1. settings의 install_apps에 rest_framework, corsheaders, users를 추가해 놓았습니다.   
4_2. settings의 middleware에 corsheaders.middleware.CorsMiddleware 추가해 놓았습니다.   
4_3. settings의 LANGUAGE_CODE, TIME_ZONE을 한국어, 서울 시간대로 변경해 놓았습니다.   
4_4. 이미지 파일 대비하여 settings에 MEDIA_ROOT를 설정해 두었습니다. (참고: https://docs.djangoproject.com/en/4.2/howto/static-files/)    
