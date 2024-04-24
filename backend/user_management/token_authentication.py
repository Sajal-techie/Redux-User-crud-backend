# from rest_framework.authentication import TokenAuthentication
# from rest_framework.exceptions import AuthenticationFailed
# from rest_framework.authtoken.models import Token

# class CustomTokenAuthentication(TokenAuthentication):
#     print('inside this class')
#     def authenticate(self, request):
#         try:
#             print(self,request.headers,'slef requedt')
#             auth_header = request.headers.get('Authorization',None)
#             print(auth_header)
#             if not auth_header:
#                 return None
#             parts = auth_header.split()
#             print(parts[0],'sdfaaksbdn')
#             if parts[0].lower() != 'bearer':
#                 return None
            
#             try:
#                 print(parts[1],'aorts 11')
#                 token = Token.objects.get(key=parts[1])
#             except Exception as e:
#                 print('token problemss',e,Token)
#                 raise AuthenticationFailed('invalid token anu mwone')
#                 return None
#             print('hailesa')
#             print(token,token.user,'return statennenedt')
#             return (token.user,token)
            
#         except Exception as e:
#             print('lololololol in custom authentication',e )
#             raise AuthenticationFailed('Invalid token')
#         return None
#         # return (token.user, token)