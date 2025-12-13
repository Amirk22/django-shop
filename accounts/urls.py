from django.urls import path


from  . import views
urlpatterns = [
    #Register
    path('register/',views.RegisterView.as_view(), name='register'),
    path('register-code/',views.VerifyRegisterView.as_view(), name='Verify'),
    path('resend_code/',views.ResendCodeView.as_view(), name='resend_code'),
    # Login , Logout
    path('login/',views.LoginView.as_view(), name='login'),
    path('logout/',views.LogoutView.as_view(), name='logout'),
    #Profile
    path('profile/',views.ProfileView.as_view(), name='profile'),
    #ForgetPassword , ChangePassword
    path('forgot-password/',views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('forgot-password-code/',views.VerifyForForgotPasswordView.as_view(), name='verify_forgot_password'),
    path('change-password/',views.ChangePasswordView.as_view(), name='change_password'),
    path('forgot-password/resend-code/',views.ResendCodeForForgotPasswordView.as_view(), name='resend_code_for_forgot_password'),
]
urlpatterns += [
    #Register
    path('api/register/', views.RegisterAPIView.as_view(), name='api_register'),
    path('api/register/verify/', views.VerifyRegisterAPIView.as_view(), name='api_verify_register'),
    # Login , Logout
    path('api/login/', views.LoginAPIView.as_view(), name='api_login'),
    path('api/logout/', views.LogoutAPIView.as_view(), name='api_logout'),
    #Profile
    path('api/profile/', views.ProfileAPIView.as_view(), name='api_profile'),
    #ForgetPassword , ChangePassword
    path('api/forgot-password/', views.ForgotPasswordAPIView.as_view(), name='api_forgot_password'),
    path('api/forgot-password/verify/', views.VerifyForgotPasswordAPIView.as_view(), name='api_verify_forgot_password'),
    path('api/forgot-password/change/', views.ChangePasswordAPIView.as_view(), name='api_change_password'),
]