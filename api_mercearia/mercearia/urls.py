from django.urls import path
from mercearia import views
from mercearia.views import UserRegistrationView, SuperuserRegistrationView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('cadastrar/<str:tipo>/', views.cadastrar, name='cadastrar-produto'),
    path('consultar', views.ConsultarTodosProdutosView.as_view(), name='conultar-todos'),
    path('consultar/<str:tipo>', views.ConsultarProdutoView.as_view(), name='consultar-tipo'),
    path('consultar/<str:tipo>/<int:id>', views.ConsultarProdutoIdView.as_view()),
    path('alterar/<str:tipo>/<int:id>', views.AlterarProdutoView.as_view(), name='alterar-produto'),
    path('alterar/<str:tipo>/<int:id>/<str:atributo>', views.atualizar_atributo, name='alterar-atributo'),
    path('excluir/<str:tipo>/<int:id>', views.excluir_produto, name='excluir-produto'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('register/superuser/', SuperuserRegistrationView.as_view(), name='superuser-registration'),
]
