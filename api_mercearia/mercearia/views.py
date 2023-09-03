from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, APIView, permission_classes
from .models import Cereal, Laticinio, Fruta, Legume, Verdura, CustomUser, CustomUserManager, AbstractBaseUser, BaseUserManager
from .serializers import CerealSerializer, LaticinioSerializer, FrutaSerializer, LegumeSerializer, VerduraSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserSerializer


def cadastrar_produto(request, tipo, serializer_class):
    serializer = serializer_class(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(f'{tipo.capitalize()} {serializer.instance.nome} cadastrado com sucesso!')
    return Response(serializer.errors, status=400)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def cadastrar(request, tipo):
    if tipo == 'cereal':
        return cadastrar_produto(request, tipo, CerealSerializer)
    elif tipo == 'laticinio':
        return cadastrar_produto(request, tipo, LaticinioSerializer)
    elif tipo == 'fruta':
        return cadastrar_produto(request, tipo, FrutaSerializer)
    elif tipo == 'legume':
        return cadastrar_produto(request, tipo, LegumeSerializer)
    elif tipo == 'verdura':
        return cadastrar_produto(request, tipo, VerduraSerializer)
    return Response('Tipo de produto não reconhecido.', status=400)



class ConsultarTodosProdutosView(APIView):
    http_method_names = ['get']
    @permission_classes([IsAuthenticated])

    def get(self, request):
        cereais = Cereal.objects.all()
        laticinios = Laticinio.objects.all()
        frutas = Fruta.objects.all()
        legumes = Legume.objects.all()
        verduras = Verdura.objects.all()
        
        # Serializando os dados usando os serializers
        cereais_serialized = CerealSerializer(cereais, many=True).data
        laticinios_serialized = LaticinioSerializer(laticinios, many=True).data
        frutas_serialized = FrutaSerializer(frutas, many=True).data
        legumes_serialized = LegumeSerializer(legumes, many=True).data
        verduras_serialized = VerduraSerializer(verduras, many=True).data
        
        result = {
            "cereais": cereais_serialized,
            "laticinios": laticinios_serialized,
            "frutas": frutas_serialized,
            "legumes": legumes_serialized,
            "verduras": verduras_serialized
        }
        
        return Response(result)


class ConsultarProdutoView(APIView):
    http_method_names = ['get']
    @permission_classes([IsAuthenticated])

    def get(self, request, tipo):
        if tipo == 'cereal':
            produtos = Cereal.objects.all()
            serializer = CerealSerializer(produtos, many=True)

        elif tipo == 'laticinio':
            produtos = Laticinio.objects.all()
            serializer = LaticinioSerializer(produtos, many=True)

        elif tipo == 'fruta':
            produtos = Fruta.objects.all()
            serializer = FrutaSerializer(produtos, many=True)

        elif tipo == 'legume':
            produtos = Legume.objects.all()
            serializer = LegumeSerializer(produtos, many=True)

        elif tipo == 'verdura':
            produtos = Verdura.objects.all()
            serializer = VerduraSerializer(produtos, many=True)

        else:
            return Response({"error": "Tipo de produto não reconhecido."}, status=400)

        return Response(serializer.data)

class ConsultarProdutoIdView(APIView):
    http_method_names = ['get']
    @permission_classes([IsAuthenticated])

    def get(self, request, tipo, id):
        if tipo == 'cereal':
            produto = get_object_or_404(Cereal, pk=id)
            serializer = CerealSerializer(produto)

        elif tipo == 'laticinio':
            produto = get_object_or_404(Laticinio, pk=id)
            serializer = LaticinioSerializer(produto)

        elif tipo == 'fruta':
            produto = get_object_or_404(Fruta, pk=id)
            serializer = FrutaSerializer(produto)

        elif tipo == 'legume':
            produto = get_object_or_404(Legume, pk=id)
            serializer = LegumeSerializer(produto)

        elif tipo == 'verdura':
            produto = get_object_or_404(Verdura, pk=id)
            serializer = VerduraSerializer(produto)

        else:
            return Response({"error": "Produto não encontrado."}, status=404)

        return Response(serializer.data)
    
    
class AlterarProdutoView(APIView):
    http_method_names = ['put']
    @permission_classes([IsAdminUser])
    
    def put(self, request, tipo, id):
        if tipo == 'cereal':
            produto = Cereal.objects.get(pk=id)
            serializer = CerealSerializer(produto, data=request.data)

        elif tipo == 'laticinio':
            produto = Laticinio.objects.get(pk=id)
            serializer = LaticinioSerializer(produto, data=request.data)

        elif tipo == 'fruta':
            produto = Fruta.objects.get(pk=id)
            serializer = FrutaSerializer(produto, data=request.data)

        elif tipo == 'legume':
            produto = Legume.objects.get(pk=id)
            serializer = LegumeSerializer(produto, data=request.data)

        elif tipo == 'verdura':
            produto = Verdura.objects.get(pk=id)
            serializer = VerduraSerializer(produto, data=request.data)

        else:
            return Response({"error": "Tipo de produto não reconhecido."}, status=400)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)


@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def atualizar_atributo(request, tipo, id, atributo):
    try:
        if tipo == 'cereal':
            produto = Cereal.objects.get(id=id)
        elif tipo == 'laticinio':
            produto = Laticinio.objects.get(id=id)
        elif tipo == 'fruta':
            produto = Fruta.objects.get(id=id)
        elif tipo == 'legume':
            produto = Legume.objects.get(id=id)
        elif tipo == 'verdura':
            produto = Verdura.objects.get(id=id)
        else:
            return Response({'error': 'Tipo de produto não reconhecido.'}, status=400)

        if hasattr(produto, atributo):
            novo_valor = request.data.get('valor')
            setattr(produto, atributo, novo_valor)
            produto.save()
            return Response({'message': f'{atributo} do {tipo.capitalize()} {id} alterado com sucesso.'}, status=200)
        else:
            return Response({'error': 'Atributo não reconhecido.'}, status=400)

    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def excluir_produto(request, tipo, id):
    produto_model = None
    if tipo == 'cereal':
        produto_model = Cereal
    elif tipo == 'laticinio':
        produto_model = Laticinio
    elif tipo == 'fruta':
        produto_model = Fruta
    elif tipo == 'legume':
        produto_model = Legume
    elif tipo == 'verdura':
        produto_model = Verdura

    if produto_model:
        produto = get_object_or_404(produto_model, id=id)
        
        if hasattr(produto, 'marca'):
            atributo = produto.marca
        elif hasattr(produto, 'tipo_fornecedor'):
            atributo = produto.tipo_fornecedor
        else:
            atributo = None
        
        produto.delete()
        return Response(f'{tipo.capitalize()} {produto.nome} {atributo} {produto.descricao} excluído com sucesso!')
    else:
        return Response(f'Tipo de produto não reconhecido.', status=400)

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SuperuserRegistrationView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'Superuser created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



