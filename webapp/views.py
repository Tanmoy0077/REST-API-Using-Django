from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum

from .models import User, FacilityDetails, WasteType, DisposalDetails, FormDetails, RequestStatus, Remarks
from .serializer import UserSerializer, FacilityDetailsSerializer, DisposalDetailsSerializer, WasteTypeSerializer, \
    FormDetailsSerializer, RequestStatusSerializer, RemarksSerializer


class UserList(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class UserDetail(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return Response(status=204)


class LoginView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        password = request.data.get('password')

        if not user_id or not password:
            return Response({'error': 'user_id and password are required'}, status=400)
        user = authenticate(request, user_id=user_id, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            designation = user.designation.lower()
            name = user.name
            facility_name = user.facility_name

            redirect_map = {
                'admin': 'admin',
                'director': 'dashboard',
                'sending engineer': 'sending-engineer',
                'receiving engineer': 'receiving-engineer',
                'sending manager': 'sending-manager',
                'receiving manager': 'receiving-manager',
                'disposing engineer': 'disposing-engineer',
                'disposing manager': 'disposing-manager'
            }

            redirect_page = redirect_map.get(designation, 'invalid-designation-page')
            return Response({
                'token': token.key,
                'redirect': redirect_page,
                'designation': designation,
                'name': name,
                'facility':facility_name
            })

        return Response({'error': 'Invalid user_id or password'}, status=401)


class LogoutView(APIView):
    def post(self, request):
        try:
            token_key = request.headers.get('Authorization', '').split(' ')[1]
            token = Token.objects.get(key=token_key)
            token.delete()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_204_NO_CONTENT)
        except Token.DoesNotExist:
            return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)


class FacilityDetailsListCreate(APIView):
    def get(self, request, format=None):
        facilities = FacilityDetails.objects.all()
        serializer = FacilityDetailsSerializer(facilities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = FacilityDetailsSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({'error': 'IntegrityError - Duplicate primary key'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FacilityDetailsDetail(APIView):
    def get_object(self, bldg_no):
        try:
            return FacilityDetails.objects.get(bldg_no=bldg_no)
        except FacilityDetails.DoesNotExist:
            return None

    def get(self, request, bldg_no, format=None):
        facility = self.get_object(bldg_no)
        if facility:
            serializer = FacilityDetailsSerializer(facility)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'Facility not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, bldg_no, format=None):
        facility = self.get_object(bldg_no)
        if facility:
            serializer = FacilityDetailsSerializer(facility, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Facility not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, bldg_no, format=None):
        facility = self.get_object(bldg_no)
        if facility:
            facility.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'Facility not found'}, status=status.HTTP_404_NOT_FOUND)


class UniqueFacilityNames(APIView):
    def get(self, request, format=None):
        unique_facilities = FacilityDetails.objects.values_list('facility_name', flat=True).distinct()
        unique_facility_list = list(unique_facilities)

        return Response(unique_facility_list, status=status.HTTP_200_OK)


class WasteTypeListCreate(APIView):
    def get(self, request, format=None):
        waste_types = WasteType.objects.all()
        serializer = WasteTypeSerializer(waste_types, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = WasteTypeSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({'error': 'IntegrityError - Duplicate primary key'}, status=status.HTTP_400_BAD_REQUEST)
            except ValidationError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WasteTypeDetail(APIView):
    def get_object(self, sl_no):
        try:
            return WasteType.objects.get(sl_no=sl_no)
        except WasteType.DoesNotExist:
            return None

    def get(self, request, sl_no, format=None):
        waste_type = self.get_object(sl_no)
        if waste_type:
            serializer = WasteTypeSerializer(waste_type)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'WasteType not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, sl_no, format=None):
        waste_type = self.get_object(sl_no)
        if waste_type:
            serializer = WasteTypeSerializer(waste_type, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'WasteType not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, sl_no, format=None):
        waste_type = self.get_object(sl_no)
        if waste_type:
            waste_type.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'WasteType not found'}, status=status.HTTP_404_NOT_FOUND)


class RequestStatusListCreateAPIView(APIView):
    def get(self, request):
        queryset = RequestStatus.objects.all()
        serializer = RequestStatusSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RequestStatusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestStatusDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return RequestStatus.objects.get(pk=pk)
        except RequestStatus.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        request_status = self.get_object(pk)
        serializer = RequestStatusSerializer(request_status)
        return Response(serializer.data)

    def put(self, request, pk):
        request_status = self.get_object(pk)
        serializer = RequestStatusSerializer(request_status, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        request_status = self.get_object(pk)
        request_status.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FacilityRequestsAPIView(APIView):
    def get(self, request, facility, *args, **kwargs):
        try:
            requests = RequestStatus.objects.filter(facility_name=facility)
            if not requests.exists():
                return Response(
                    {'error': 'No requests found for the specified facility.'},
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = RequestStatusSerializer(requests, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': 'An unexpected error occurred.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ReceiverApprovalAPIView(APIView):
    def get(self, request, approval, *args, **kwargs):
        try:
            requests = RequestStatus.objects.filter(receiver_approval=approval)
            if not requests.exists():
                return Response(
                    {'error': 'No requests found for the specified facility.'},
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = RequestStatusSerializer(requests, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': 'An unexpected error occurred.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# FormDetails API View
class FormDetailsListCreateAPIView(APIView):
    def get(self, request):
        queryset = FormDetails.objects.all()
        serializer = FormDetailsSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FormDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FormDetailsAPIView(APIView):
    def get_object(self, pk):
        try:
            return FormDetails.objects.get(pk=pk)
        except FormDetails.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        form_details = self.get_object(pk)
        serializer = FormDetailsSerializer(form_details)
        return Response(serializer.data)

    def put(self, request, pk):
        form_details = self.get_object(pk)
        serializer = FormDetailsSerializer(form_details, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        form_details = self.get_object(pk)
        form_details.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FormDetailsListView(generics.ListAPIView):
    serializer_class = FormDetailsSerializer

    def get_queryset(self):
        request_no = self.kwargs.get('request_no')
        return FormDetails.objects.filter(request_no=request_no)


# DisposalDetails API View
class DisposalDetailsListCreateAPIView(APIView):
    def get(self, request):
        queryset = DisposalDetails.objects.all()
        serializer = DisposalDetailsSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DisposalDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DisposalDetailsAPIView(APIView):
    def get_object(self, pk):
        try:
            return DisposalDetails.objects.get(pk=pk)
        except DisposalDetails.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        disposal_details = self.get_object(pk)
        serializer = DisposalDetailsSerializer(disposal_details)
        return Response(serializer.data)

    def put(self, request, pk):
        disposal_details = self.get_object(pk)
        serializer = DisposalDetailsSerializer(disposal_details, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        disposal_details = self.get_object(pk)
        disposal_details.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RemarksListCreateView(generics.ListCreateAPIView):
    queryset = Remarks.objects.all()
    serializer_class = RemarksSerializer


class RemarksRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Remarks.objects.all()
    serializer_class = RemarksSerializer


class PropellantDataView(APIView):
    def get(self, request, *args, **kwargs):
        units = ['U1', 'U2']
        waste_types = ['A', 'B', 'C', 'D', 'E']

        def calculate_totals(unit, data):
            available_data = DisposalDetails.objects.filter(unit=unit).values('waste_type').annotate(
                total_stored_qty=Sum('stored_qty'),
                total_disposed_qty=Sum('disposed_qty')
            )
            stored_total = {waste_type: 0 for waste_type in waste_types}
            disposed_total = {waste_type: 0 for waste_type in waste_types}
            
            for item in available_data:
                print(item)
                if item['waste_type'] in stored_total:
                    stored_total[item['waste_type']] = item['total_stored_qty']
                    disposed_total[item['waste_type']] = item['total_disposed_qty']
            if data == "stored":
                return stored_total
            
            return disposed_total


        available_data = {unit: calculate_totals(unit, "stored") for unit in units}
        disposed_data = {unit: calculate_totals(unit, "disposed") for unit in units}


        return Response({
            'availableData': available_data,
            'disposedData': disposed_data
        }, status=status.HTTP_200_OK)
