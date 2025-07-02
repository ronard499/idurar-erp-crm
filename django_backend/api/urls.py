from django.urls import path
from . import views
from . import auth

# Core auth routes
urlpatterns = [
    # Auth routes
    path('login', auth.login, name='login'),
    path('logout', auth.logout, name='logout'),
    path('forgetpassword', auth.forget_password, name='forget_password'),
    path('resetpassword', auth.reset_password, name='reset_password'),
    
    # Client routes
    path('client/create', views.create_client, name='create_client'),
    path('client/read/<uuid:id>', views.read_client, name='read_client'),
    path('client/update/<uuid:id>', views.update_client, name='update_client'),
    path('client/delete/<uuid:id>', views.delete_client, name='delete_client'),
    path('client/list', views.list_clients, name='list_clients'),
    path('client/listAll', views.list_all_clients, name='list_all_clients'),
    path('client/filter', views.filter_clients, name='filter_clients'),
    path('client/search', views.search_clients, name='search_clients'),
    path('client/summary', views.client_summary, name='client_summary'),
    
    # PaymentMode routes
    path('paymentMode/create', views.create_payment_mode, name='create_payment_mode'),
    path('paymentMode/read/<uuid:id>', views.read_payment_mode, name='read_payment_mode'),
    path('paymentMode/update/<uuid:id>', views.update_payment_mode, name='update_payment_mode'),
    path('paymentMode/delete/<uuid:id>', views.delete_payment_mode, name='delete_payment_mode'),
    path('paymentMode/list', views.list_payment_modes, name='list_payment_modes'),
    path('paymentMode/listAll', views.list_all_payment_modes, name='list_all_payment_modes'),
    path('paymentMode/filter', views.filter_payment_modes, name='filter_payment_modes'),
    path('paymentMode/search', views.search_payment_modes, name='search_payment_modes'),
    
    # Product routes
    path('product/create', views.create_product, name='create_product'),
    path('product/read/<uuid:id>', views.read_product, name='read_product'),
    path('product/update/<uuid:id>', views.update_product, name='update_product'),
    path('product/delete/<uuid:id>', views.delete_product, name='delete_product'),
    path('product/list', views.list_products, name='list_products'),
    path('product/listAll', views.list_all_products, name='list_all_products'),
    path('product/filter', views.filter_products, name='filter_products'),
    path('product/search', views.search_products, name='search_products'),
    
    # Quote routes
    path('quote/create', views.create_quote, name='create_quote'),
    path('quote/read/<uuid:id>', views.read_quote, name='read_quote'),
    path('quote/update/<uuid:id>', views.update_quote, name='update_quote'),
    path('quote/delete/<uuid:id>', views.delete_quote, name='delete_quote'),
    path('quote/list', views.list_quotes, name='list_quotes'),
    path('quote/listAll', views.list_all_quotes, name='list_all_quotes'),
    path('quote/filter', views.filter_quotes, name='filter_quotes'),
    path('quote/search', views.search_quotes, name='search_quotes'),
    path('quote/summary', views.quote_summary, name='quote_summary'),
    path('quote/convert/<uuid:id>', views.convert_quote_to_invoice, name='convert_quote_to_invoice'),
    path('quote/mail', views.mail_quote, name='mail_quote'),
    
    # Invoice routes
    path('invoice/create', views.create_invoice, name='create_invoice'),
    path('invoice/read/<uuid:id>', views.read_invoice, name='read_invoice'),
    path('invoice/update/<uuid:id>', views.update_invoice, name='update_invoice'),
    path('invoice/delete/<uuid:id>', views.delete_invoice, name='delete_invoice'),
    path('invoice/list', views.list_invoices, name='list_invoices'),
    path('invoice/listAll', views.list_all_invoices, name='list_all_invoices'),
    path('invoice/filter', views.filter_invoices, name='filter_invoices'),
    path('invoice/search', views.search_invoices, name='search_invoices'),
    path('invoice/summary', views.invoice_summary, name='invoice_summary'),
    path('invoice/mail', views.mail_invoice, name='mail_invoice'),
    
    # Payment routes
    path('payment/create', views.create_payment, name='create_payment'),
    path('payment/read/<uuid:id>', views.read_payment, name='read_payment'),
    path('payment/update/<uuid:id>', views.update_payment, name='update_payment'),
    path('payment/delete/<uuid:id>', views.delete_payment, name='delete_payment'),
    path('payment/list', views.list_payments, name='list_payments'),
    path('payment/listAll', views.list_all_payments, name='list_all_payments'),
    path('payment/filter', views.filter_payments, name='filter_payments'),
    path('payment/search', views.search_payments, name='search_payments'),
    path('payment/summary', views.payment_summary, name='payment_summary'),
    path('payment/mail', views.mail_payment, name='mail_payment'),
    
    # Settings routes
    path('setting', views.settings, name='settings'),
    path('setting/<str:key>', views.settings, name='settings_key'),
]