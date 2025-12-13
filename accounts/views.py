import string

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login
from django.shortcuts import render , redirect ,reverse
from django.views import View
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .froms import RegisterForm, RegisterActiveCodeForm,LoginForm, ForgotPasswordForm, ForgotPasswordCodeForm,ChangePasswordForm
from .models import User
import secrets
from django.core.cache import cache
from django.core.mail import send_mail
from django.contrib.auth import login,logout
from django.contrib import messages
from django.utils.decorators import method_decorator
from .decorators import require_pending_email, require_password_change
from .decorators import logout_required
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework import permissions
from accounts.tasks import send_verification_email

from .serializers import RegisterSerializer , VerifySerializer ,LoginSerializer , ForgotPasswordSerializer ,ChangePasswordSerializer ,ForgotPasswordCodeSerializer,ProfileSerializer


# Create your views here.


def generate_5digit_code():
    return ''.join(secrets.choice(string.digits) for _ in range(5))

#..................................................................................................................Template

#......................................................... register
@method_decorator(logout_required(redirect_url='home_page'), name='dispatch')
class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'account/register.html', {'register_form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].strip().lower()
            password = form.cleaned_data['password']

            if User.objects.filter(email__iexact=email).exists():
                form.add_error('email', 'این کاربر قبلا ثبت نام کرده است')
            else:
                request.session['register_data'] = {'email': email, 'password': password}
                code = str(generate_5digit_code())
                key = f"activation_{email}"
                cache.set(key, code, timeout=120)
                request.session['pending_user_email'] = email


                send_verification_email.delay(
                    email,
                    'کد فعال‌سازی حساب',
                    f'کد فعال‌سازی شما: {code}',
                    'noreply@yourdomain.com'
                )

                return redirect(reverse('Verify'))

        return render(request, 'account/register.html', {'register_form': form})

class VerifyRegisterView(View):
    @method_decorator(require_pending_email('pending_user_email', 'register'))
    def get(self, request):
        form = RegisterActiveCodeForm()
        return render(request, 'account/verify.html', {
            'register_active_code_form': form,
            'error': None,
            'message': None
        })

    @method_decorator(require_pending_email('pending_user_email', 'register'))
    def post(self, request):
        form = RegisterActiveCodeForm(request.POST)
        email = request.session.get('pending_user_email')
        if not email:
            return redirect('register')
        error = None

        if form.is_valid():
            code = form.cleaned_data['code'].strip()
            key = f"activation_{email}"
            saved_code = cache.get(key)

            if saved_code and saved_code == code:
                data = request.session.get('register_data')
                if data:
                    user = User.objects.create_user(
                        username=email,
                        email=email,
                        password=data['password']
                    )
                    login(request, user)
                    cache.delete(key)
                    request.session.pop('pending_user_email', None)
                    request.session.pop('register_data', None)
                    return redirect('home_page')
                else:
                    error = 'مشکل در داده‌های ثبت‌نام.'
            else:
                error = 'کد اشتباه یا منقضی شده است.'
        else:
            error = 'فرم نامعتبر است.'

        return render(request, 'account/verify.html', {
            'register_active_code_form': form,
            'error': error
        })

class ResendCodeView(View):
    def post(self, request):
        email = request.session.get('pending_user_email')
        if not email:
            return redirect('register')

        code = str(generate_5digit_code())
        key = f"activation_{email}"
        cache.set(key, code, timeout=120)

        send_verification_email.delay(
            email,
            'کد فعال‌سازی حساب',
            f'کد فعال‌سازی شما: {code}',
            'noreply@yourdomain.com'
        )

        messages.success(request, 'کد جدید برای شما ارسال شد.')
        return redirect('Verify')
#......................................................... login
@method_decorator(logout_required(redirect_url='home_page'), name='dispatch')
class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        return render(request, 'account/login.html', {'login_form': login_form})

    def post(self, request):
        login_form = LoginForm(request.POST)
        error = None

        if login_form.is_valid():
            email = login_form.cleaned_data['email'].strip().lower()
            password = login_form.cleaned_data['password']

            user = User.objects.filter(email__iexact=email).first()
            if user is not None:
                if user.check_password(password):
                    login(request, user)
                    return redirect(reverse('home_page'))
                else:
                    error = 'رمز عبور اشتباه است.'
            else:
                error = 'کاربری با این ایمیل وجود ندارد.'
        else:
            error = 'فرم نامعتبر است.'

        return render(request, 'account/login.html', {
            'login_form': login_form,
            'error': error
        })

#......................................................... logout
@method_decorator(login_required, name='dispatch')
class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect(reverse('home_page'))

#......................................................... forgot_password
@method_decorator(logout_required(redirect_url='home_page'), name='dispatch')
class ForgotPasswordView(View):
    def get(self, request):
        form = ForgotPasswordForm()
        return render(request, 'account/forgot_password.html', {'ForgotPasswordForm': form})
    def post(self, request):
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].strip().lower()
            if User.objects.filter(email__iexact=email).exists():
                request.session['register_data'] = {'email': email}
                code = str(generate_5digit_code())
                key = f"activation_{email}"
                cache.set(key, code, timeout=120)
                send_verification_email.delay(
                    email,
                    'کد فعال‌سازی حساب',
                    f'کد فعال‌سازی شما: {code}',
                    'noreply@yourdomain.com'
                )


                request.session['pending_user_email'] = email
                return redirect(reverse('verify_forgot_password'))
            else:
                form.add_error('email', 'این کاربر قبلا ثبت نام نکرده است')

        return render(request, 'account/forgot_password.html', {'ForgotPasswordForm': form})

class VerifyForForgotPasswordView(View):
    @method_decorator(require_pending_email('pending_user_email', 'forgot_password'))
    def get(self, request):
        form = ForgotPasswordCodeForm()
        return render(request, 'account/verify_forgot_password.html', {'ForgotPasswordCodeForm': form})

    @method_decorator(require_pending_email('pending_user_email', 'forgot_password'))
    def post(self, request):
        form = ForgotPasswordCodeForm(request.POST)
        email = request.session.get('pending_user_email')
        if not email:
            return redirect('forgot_password')
        if form.is_valid():
            code = form.cleaned_data['code'].strip()
            key = f"activation_{email}"
            saved_code = cache.get(key)
            if saved_code and saved_code == code:
                request.session['allow_password_change'] = True
                return redirect(reverse('change_password'))
        return render(request, 'account/verify_forgot_password.html', {'ForgotPasswordCodeForm': form})

class ChangePasswordView(View):
    @method_decorator(require_password_change())
    def get(self, request):
        form = ChangePasswordForm()
        email = request.session.get('pending_user_email')
        error = None
        if not email:
            error = 'کد اشتباه یا منقضی شده است.'
        return render(request, 'account/change_forgot_password.html', {
            'ChangePasswordForm': form,
            'error': error
        })

    @method_decorator(require_password_change())
    def post(self, request):
        form = ChangePasswordForm(request.POST)
        email = request.session.get('pending_user_email')
        error = None

        if not email:
            error = 'کد اشتباه یا منقضی شده است.'
        elif form.is_valid():
            password = form.cleaned_data['password']
            user = User.objects.filter(email=email).first()
            if user:
                user.set_password(password)
                user.save()
                request.session.pop('pending_user_email', None)
                return redirect('login')

        return render(request, 'account/change_forgot_password.html', {
            'ChangePasswordForm': form,
            'error': error
        })

class ResendCodeForForgotPasswordView(View):
    def post(self, request):
        email = request.session.get('pending_user_email')
        if not email:
            return redirect('forgot_password')


        code = str(generate_5digit_code())
        key = f"activation_{email}"
        cache.set(key, code, timeout=120)

        send_verification_email.delay(
            email,
            'کد فعال‌سازی حساب',
            f'کد فعال‌سازی شما: {code}',
            'noreply@yourdomain.com'
        )

        message = 'کد جدید برای شما ارسال شد.'

        form = ForgotPasswordCodeForm()
        return render(request, 'account/verify_forgot_password.html', {
            'ForgotPasswordCodeForm': form,
            'message': message
        })

#......................................................... profile
@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        return render(request, 'account/profile.html', {'user': request.user})


#..................................................................................................................API

#......................................................... register

class RegisterAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email'].lower()
            password = serializer.validated_data['password']

            if User.objects.filter(email__iexact=email).exists():
                return Response({'error': 'این کاربر قبلا ثبت نام کرده است'}, status=400)

            cache.set(f"register_data_{email}", {'email': email, 'password': password}, timeout=300)

            code = str(generate_5digit_code())
            key = f"activation_{email}"
            cache.set(key, code, timeout=120)

            send_mail(
                'کد فعال‌سازی حساب',
                f'کد فعال‌سازی شما: {code}',
                'noreply@yourdomain.com',
                [email],
                fail_silently=False,
            )


            return Response({'message': 'کد فعال‌سازی ارسال شد'}, status=200)

        return Response(serializer.errors, status=400)

class VerifyRegisterAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = VerifySerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email'].lower()
            code = serializer.validated_data['code'].strip()

            saved_code = cache.get(f"activation_{email}")
            data = cache.get(f"register_data_{email}")

            if not saved_code or not data:
                return Response({'error': 'کد منقضی شده است'}, status=400)

            if saved_code != code:
                return Response({'error': 'کد اشتباه است'}, status=400)

            user = User.objects.create_user(
                username=email,
                email=email,
                password=data['password']
            )

            cache.delete(f"activation_{email}")
            cache.delete(f"register_data_{email}")

            return Response({'message': 'ثبت‌نام با موفقیت انجام شد'}, status=201)

        return Response(serializer.errors, status=400)

#......................................................... login
class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email'].strip().lower()
            password = serializer.validated_data['password']

            user = authenticate(username=email, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'message': 'ورود موفق',
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                }, status=200)
            return Response({'error': 'ایمیل یا رمز اشتباه است'}, status=400)
        return Response(serializer.errors, status=400)

#......................................................... logout
class LogoutAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            token = RefreshToken(request.data.get('refresh'))
            token.blacklist()
            return Response({'message': 'خروج موفق'}, status=200)
        except Exception:
            return Response({'error': 'توکن نامعتبر است'}, status=400)

#......................................................... forgot_password
class ForgotPasswordAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email'].lower()

            if not User.objects.filter(email=email).exists():
                return Response({'error': 'کاربر وجود ندارد'}, status=400)

            code = generate_5digit_code()
            cache.set(f"forgot_{email}", code, timeout=300)

            send_mail(
                'کد بازیابی رمز عبور',
                f'کد شما: {code}',
                'noreply@yourdomain.com',
                [email],
                fail_silently=False,
            )

            return Response({'message': 'کد ارسال شد'}, status=200)
        return Response(serializer.errors, status=400)
0
class VerifyForgotPasswordAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ForgotPasswordCodeSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email'].lower()
            code = serializer.validated_data['code'].strip()

            saved_code = cache.get(f"forgot_{email}")
            if saved_code and saved_code == code:
                cache.set(f"allow_reset_{email}", True, timeout=300)
                return Response({'message': 'کد صحیح است، رمز جدید را وارد کنید'}, status=200)
            return Response({'error': 'کد اشتباه یا منقضی شده است'}, status=400)
        return Response(serializer.errors, status=400)

class ChangePasswordAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email'].lower()
            new_password = serializer.validated_data['password']

            if not cache.get(f"allow_reset_{email}"):
                return Response({'error': 'دسترسی برای تغییر رمز ندارید'}, status=400)

            user = User.objects.filter(email=email).first()
            if not user:
                return Response({'error': 'کاربر پیدا نشد'}, status=400)
            user.password = make_password(new_password)
            user.save()
            cache.delete(f"allow_reset_{email}")
            return Response({'message': 'رمز عبور با موفقیت تغییر کرد'}, status=200)
        return Response(serializer.errors, status=400)


#......................................................... profile
class ProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data, status=200)



