from rest_framework import viewsets
from .models import *
from .serializer import *
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.permissions import IsAuthenticated




class IdTypeView(viewsets.ModelViewSet):
    queryset = IdType.objects.all()
    serializer_class = IdTypeSerializer


class CountryView(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class StateView(viewsets.ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer


class CityView(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class AddressView(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class ProgramView(viewsets.ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer


class ProgramParticipantView(viewsets.ModelViewSet):
    queryset = ProgramParticipant.objects.all()
    serializer_class = ProgramParticipantSerializer


class RequestView(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer


class ProposerStatusView(viewsets.ModelViewSet):
    queryset = ProposerStatus.objects.all()
    serializer_class = ProposerStatusSerializer




class BatchStatusView(viewsets.ModelViewSet):
    queryset = BatchStatus.objects.all()
    serializer_class = BatchStatusSerializer


class BatchView(viewsets.ModelViewSet):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer


class BatchLearnerView(viewsets.ModelViewSet):
    queryset = BatchLearner.objects.all()
    serializer_class = BatchLearnerSerializer


class AssignmentView(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer


class JobReadinessView(viewsets.ModelViewSet):
    queryset = JobReadiness.objects.all()
    serializer_class = JobReadinessSerializer


class JobApplicationView(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer


class EnablerSponsorView(viewsets.ModelViewSet):
    queryset = EnablerSponsor.objects.all()
    serializer_class = EnablerSponsorSerializer


class EnablerTrainerView(viewsets.ModelViewSet):
    queryset = EnablerTrainer.objects.all()
    serializer_class = EnablerTrainerSerializer


class LearnerRoleView(viewsets.ModelViewSet):
    queryset = LearnerRole.objects.all()
    serializer_class = LearnerRoleSerializer
    
    
    
    
class LearnerView(viewsets.ModelViewSet):
    queryset = Learner.objects.all()
    serializer_class = LearnerSerializer


class EnablerView(viewsets.ModelViewSet):
    queryset = Enabler.objects.all()
    serializer_class = EnablerSerializer







class SponsorView(viewsets.ModelViewSet):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer 
    permission_classes = [IsAuthenticated] 

    @action(detail=True, methods=['post'])
    def approve_learner(self, request, pk=None):
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required."}, status=401)

        sponsor = self.get_object()

        
        user = request.user
        
        status_name = request.data.get('approval_status')
        try:
            status_instance = ProposerStatus.objects.get(name=status_name)
        except ProposerStatus.DoesNotExist:
            return Response(
                {"error": f"ProposerStatus with name `{status_name}` does not exist."},
                status=400
            )

        
        if user.role and user.role.name != 'LEARNER':
           
            learner_role, created = Role.objects.get_or_create(name="LEARNER")
            user.role = learner_role
            user.save()

        
        
        send_mail(
            subject="Learner Approved",
            message=f"Dear {user.first_name},\n\nThe learner with email {user.email} has been approved and their role has been updated to 'LEARNER'.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[sponsor.requestor.user.email],
            fail_silently=False,
        )

        
        send_mail(
            subject="Your Role Has Been Updated to LEARNER",
            message=f"Dear {user.first_name},\n\nCongratulations!Your role has been updated to 'LEARNER'.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        
        sponsor_serializer = self.get_serializer(sponsor)
        
        
        return Response({
            "sponsor": sponsor_serializer.data,
            
            "user": {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "role":  user.role.name if user.role else None,
                "approval_status": status_instance.name 
            }
        })
            
        
    


class TrainerView(viewsets.ModelViewSet):
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer
    
