from django.conf import settings
from django.conf.urls.static import static
from . forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm
from django.urls import path
from Shop import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home.as_view(), name='home'),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.CustomerProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minuscart),
    path('removecart/', views.remove_cart),
    path('search/', views.search, name='search'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='Shop/passwordchange.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'), name='password_change'),
    path('passwordchangedone/', auth_views.PasswordChangeView.as_view(template_name='Shop/passwordchangedone.html'), name='passwordchangedone'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='Shop/password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='Shop/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='Shop/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='Shop/password_reset_complete.html'), name='password_reset_complete'),

    path('lehenga/', views.lehenga, name='lehenga'),
    path('lehenga/<slug:data>', views.lehenga, name='lehengaitem'),
    path('saree/', views.saree, name='saree'),
    path('saree/<slug:data>', views.saree, name='sareeitem'),
    path('borkha/', views.borkha, name='borkha'),
    path('borkha/<slug:data>', views.borkha, name='borkhaitem'),
    path('baby_fashion/', views.baby_fashion, name='baby_fashion'),
    path('baby_fashion/<slug:data>', views.baby_fashion, name='baby_fashionitem'),
    path('pants/', views.pants, name='pants'),
    path('pants/<slug:data>', views.pants, name='pantsitem'),

    path('accounts/login/', auth_views.LoginView.as_view(template_name='Shop/login.html', authentication_form=LoginForm), name='loginpage'),
    path('registration/', views.customerregistration.as_view(), name='customerregistration'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.paymentdone, name='paymentdone'),
    path('logout/', auth_views.LogoutView.as_view(next_page='loginpage'), name='logout'),
    path('success/', views.successful.as_view(), name ='successful'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)