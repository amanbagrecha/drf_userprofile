from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from quickstart.models import userprofile
from .serializers import userprofileSerializer


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import  permission_classes
from django.core.exceptions import ObjectDoesNotExist
import json
from quickstart.forms import UserForm
#start

# get all users
@api_view(["GET"])
@csrf_exempt
# @permission_classes([IsAuthenticated])
def get_users(request):
    user_profile = userprofile.objects.all() # additional filter: filter(added_by=request.user)
    serializer = userprofileSerializer(user_profile, many=True)
    return JsonResponse({'user_profile': serializer.data}, safe=False, status=status.HTTP_200_OK)

# get given user
@api_view(['GET'])
@csrf_exempt
def get_given_user(request, pk):
    
    try:
        user_profile = userprofile.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return JsonResponse({"missing": ""}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':  # not necessary here
        serializer = userprofileSerializer(user_profile)
        return JsonResponse({'given_user_profile': serializer.data})
   

# update user
@api_view(["PUT",]) # have to first request via get, only then put
@csrf_exempt
@permission_classes([IsAuthenticated])
def update_user(request, pk):
    try:
        user_profile = userprofile.objects.get(id=pk)
    except ObjectDoesNotExist:
        return Response({'response': "given object does not exist"}, status=status.HTTP_404_NOT_FOUND)

    user = request.user
    # this works only when authentication token is passed
    if user_profile.author != user:
        return JsonResponse({'response':"You don't have permission to edit that."}, safe=False)
        
    # data= { "id": pk, "email": 'changed@gmail.com'}

    # return JsonResponse({'Error:' : 'You are not Authorized to access this page'}, safe=False) 
    # serializer = userprofileSerializer( data=request.query_params)
    # print(request.query_params, (  {i:j for i,j in request.query_params.items()}  ))
    data =  {i:j for i,j in request.query_params.items()}
    try:
        userprofile.objects.filter(id=pk).update(**data)  #retuns 1 or 0; using get() returns single object, and that is why update doesnt work
        user_profile = userprofile.objects.get(id=pk)
        serializer = userprofileSerializer(user_profile)
        return JsonResponse({'user_update': serializer.data}, safe=False, status=status.HTTP_200_OK)  # input must be json object. user_profile wont respond
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# delete user
@api_view(["DELETE",'GET']) # have to first request via `get`, only then `put`
@csrf_exempt
@permission_classes([IsAuthenticated])
def delete_user(request, pk):

    try:
        user_profile = userprofile.objects.get(id=pk)
    except ObjectDoesNotExist:
        return JsonResponse({'response': "given object does not exist"}, safe=False, status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if user_profile.author != user:  # this works only when authentication token is passed
        return JsonResponse({'response':"You don't have permission to edit that."}, safe=False)

    try:
        userprofile.objects.get(id=pk).delete()  #retuns 1 or 0
        return JsonResponse({'user_delete': "record deleted"}, safe=False, status=status.HTTP_200_OK)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# end



















""" example input for userprofile model
{
    "id":2,
    "email": "ajax@gmail.cpm",
    "name": "ajasx",
    "password":"ajax@1234"
}
"""
































# add post
# @permission_classes([IsAuthenticated])
 
# @api_view(["POST", "GET"])
# @csrf_exempt
# def add_user(request):
#         data= {"id": 1, "email": "dddd@gmail.com", "name": "aman", "password": "3333asdas"}
#         try:
#             # author = Author.objects.get(id=payload["author"])
#             user_profile = userprofile.objects.create(**data)
#             serializer = userprofileSerializer(user_profile)
#             return JsonResponse({'added_users': serializer.data}, safe=False, status=status.HTTP_201_CREATED)
#         except ObjectDoesNotExist as e:
#             return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
#         except Exception:
#             return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)













# get given user
# @api_view(['GET'],)
# def user_detail_view(request, pk):
    
#     try:
#         user_profile = userprofile.objects.get(pk=pk)
#     except userprofile.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         # user_profile = userprofile.objects.all()
#         serializer = userprofileSerializer(user_profile)
#         return Response(serializer.data)
   


# add user
@csrf_exempt
# @permission_classes([IsAuthenticated])
@api_view(['POST'])
def user_add_view(request):

        
        serializer = userprofileSerializer( data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # try:
    #     user_profile = userprofile.objects.all()
    # except userprofile.DoesNotExist:
    #     return Response(status=status.HTTP_404_NOT_FOUND)

    # if request.method == 'GET':
    #     # user_profile = userprofile.objects.all()
    #     serializer = userprofileSerializer(user_profile, many=True)
    #     return Response(serializer.data)

    # if request.method == 'POST':
        # data = JSONParser().parse(request)



# update given user
# @api_view(['PUT', 'GET'])
# def user_edit_view(request,pk):
#         try:
#             user_profile = userprofile.objects.get(pk=pk)
#         except userprofile.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
    
#         if request.method == 'GET':
#             # user_profile = userprofile.objects.all()
#             serializer = userprofileSerializer(user_profile)
#             return Response(serializer.data)
        
#     # if request.method == 'PUT':
#         # data ={
#         # "id": 1,
#         # "email": "SS@gmail.com",
#         # "name": "fgb",
#         # "password": "3333"
#         #     }
#         serializer = userprofileSerializer(user_profile, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# delete given user
# @api_view(['DELETE', 'GET'],)
# def user_delete_view(request,pk):
#     try:
#         user_profile = userprofile.objects.get(pk=pk)
#     except userprofile.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         # user_profile = userprofile.objects.all()
#         serializer = userprofileSerializer(user_profile)
#         return Response(serializer.data)
#     if request.method == 'DELETE':
#         user_profile.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)  
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# get all users
# @api_view(['GET'],)
# def user_view(request):
    
#     try:
#         user_profile = userprofile.objects.all()
#     except userprofile.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         # user_profile = userprofile.objects.all()
#         serializer = userprofileSerializer(user_profile, many=True)
#         return Response(serializer.data)

