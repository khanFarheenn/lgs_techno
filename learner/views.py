from rest_framework import viewsets
from .models import *
from .serializer import *

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


class TrainerView(viewsets.ModelViewSet):
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer
    
