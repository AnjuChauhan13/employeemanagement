from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions,pagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Employee
from .serializers import EmployeeSerializer
from rest_framework.pagination import PageNumberPagination



class EmployeeViewset(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        department = request.GET.get('department', None)
        position = request.GET.get('position', None)
        search = request.GET.get('search', None)
        employees = Employee.objects.all()
        if department:
            employees = employees.filter(department__iexact=department)  
        if position:
            employees = employees.filter(position__iexact=position)
        if search:
            employees = employees.filter(
                Q(full_name__icontains=search) | Q(position__icontains=search)
            )  

        paginator = PageNumberPagination()
        paginated_employees = paginator.paginate_queryset(employees, request)
        serializer = EmployeeSerializer(paginated_employees, many=True)

        return paginator.get_paginated_response(serializer.data)
    
    def post(self, request):
        if not request.user.is_staff:
            return Response({'error': 'Only admins can create employees'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        employee = self.get_object(pk)
        if not employee:
            return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

        if not request.user.is_staff:
            return Response({'error': 'Only admins can update employees'}, status=status.HTTP_403_FORBIDDEN)

        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, pk):
        employee = self.get_object(pk)
        if not employee:
            return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

        if not request.user.is_staff:
            return Response({'error': 'Only admins can delete employees'}, status=status.HTTP_403_FORBIDDEN)

        employee.delete()
        return Response({'message': 'Employee deleted successfully'}, status=status.HTTP_204_NO_CONTENT)