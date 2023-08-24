from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .serializers import PasswordResetSerializer, UserSerializer
from rest_framework import generics


class CheckFirstTimeLoginView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_first_time:
            return Response({'is_first_time': True, 'message': 'First-time login. Please reset your password.'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'is_first_time': False, 'message': 'Not a first-time login.'}, status=status.HTTP_200_OK)


User = get_user_model()


class ResetPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if new_password and confirm_password:
            if new_password == confirm_password:
                user.set_password(new_password)
                user.is_first_time = False
                user.save()
                return Response({'message': 'Password reset successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'New password and confirm password do not match.'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Empty passwords '}, status=status.HTTP_400_BAD_REQUEST)


class ProfileResetPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        current_password = serializer.validated_data['current_password']
        new_password = serializer.validated_data['new_password']
        confirm_password = serializer.validated_data['confirm_password']

        if current_password and new_password and confirm_password:
            if not user.check_password(current_password):
                return Response({'error': 'Current password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'New password and confirm password do not match.'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Please provide all fields'},
                            status=status.HTTP_400_BAD_REQUEST)


class UserListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
