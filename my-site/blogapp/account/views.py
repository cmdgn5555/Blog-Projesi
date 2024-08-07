from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User


# Create your views here.

def login_request(request):
   
    max_deneme_hakki = 3
    engelleme_suresi = 30

    if 'deneme' not in request.session:
        request.session['deneme'] = 0
    
    if 'engelleme_zamani' in request.session:
        engelleme_zamani_str = request.session['engelleme_zamani']
        engelleme_zamani = timezone.datetime.fromisoformat(engelleme_zamani_str)


        if timezone.now() < engelleme_zamani:
            kalan_sure = (engelleme_zamani - timezone.now()).seconds
            return render(request, "account/login.html", {
                "error": f"Hesabınız çok fazla başarısız giriş denemesi nedeniyle kilitlendi. Lütfen {kalan_sure} saniye sonra tekrar deneyin."
            })
        
        else:
            del request.session['engelleme_zamani']
            request.session['deneme'] = 0
        
    
    if request.user.is_authenticated:
        return redirect("ana")
    
    if request.method == "POST":
        kullanici_adi = request.POST.get("username")
        sifre = request.POST.get("password")
        
        if kullanici_adi and sifre:
            kullanici = authenticate(request, username=kullanici_adi, password=sifre)

            if kullanici is not None:
                login(request, kullanici)
                request.session['deneme'] = 0
                return redirect("ana")
        
            else:
                request.session['deneme'] += 1
            
                if request.session['deneme'] >= max_deneme_hakki:
                    engelleme_zamani = timezone.now() + timedelta(seconds=engelleme_suresi)
                    request.session['engelleme_zamani'] = engelleme_zamani.isoformat()
                    return render(request, "account/login.html", {
                        "error":"3 kere hatalı giriş yaptınız..."
                    })
    
                return render(request, "account/login.html", {
                    "error": f"Kullanıcı adınız ya da şifreniz yanlış!!! ({request.session['deneme']} / {max_deneme_hakki})"
                })
        else:
            return render(request, "account/login.html", {
                "error": "Lütfen kullanıcı adı ve şifre alanlarını doldurun."
            })
    
    return render(request, "account/login.html")



def register_request(request):
    
    if request.user.is_authenticated:
        return redirect("ana")
    
    if request.method == "POST":
        kullanici_adi = request.POST.get("username")
        eposta = request.POST.get("email")
        ad = request.POST.get("firstname")
        soyad = request.POST.get("lastname")
        parola = request.POST.get("password")
        parola_tekrari = request.POST.get("repassword")

        if parola == parola_tekrari:
            if User.objects.filter(username=kullanici_adi).exists():
                return render(request, "account/register.html", {
                    "error": "bu kullanıcı adı zaten kullanılıyor!!!",
                    "u_name": kullanici_adi,
                    "e_mail": eposta,
                    "f_name": ad,
                    "l_name": soyad,
                    "pass": parola,
                    "repass": parola_tekrari,
                })
            
            else:
                if User.objects.filter(email=eposta).exists():
                    return render(request, "account/register.html", {
                        "error": "bu eposta zaten kullanılıyor!!!",
                        "u_name": kullanici_adi,
                        "e_mail": eposta,
                        "f_name": ad,
                        "l_name": soyad,
                        "pass": parola,
                        "repass": parola_tekrari,
                    })
                
                else:
                    kullanici = User.objects.create_user(
                        username=kullanici_adi,
                        email=eposta,
                        first_name=ad,
                        last_name=soyad,
                        password=parola
                    )
                    kullanici.save()
                    return redirect("giris")
        else:
            return render(request, "account/register.html", {
                "error": "parola eşleşmiyor!!!",
                "u_name": kullanici_adi,
                "e_mail": eposta,
                "f_name": ad,
                "l_name": soyad,
                "pass": parola,
                "repass": parola_tekrari,
            })

    return render(request, "account/register.html")


def logout_request(request):
    
    logout(request)
    
    return redirect("ana")
