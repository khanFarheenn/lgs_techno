from rest_framework import serializers
from .models import *

class IdTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdType
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = '__all__'


class ProgramParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramParticipant
        fields = '__all__'


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'


class ProposerStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProposerStatus
        fields = '__all__'


class LearnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Learner
        fields = '__all__'


class EnablerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enabler
        fields = '__all__'


class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = '__all__'


class TrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainer
        fields = '__all__'


class BatchStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatchStatus
        fields = '__all__'


class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = '__all__'


class BatchLearnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatchLearner
        fields = '__all__'


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'


class JobReadinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobReadiness
        fields = '__all__'


class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = '__all__'


class EnablerSponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnablerSponsor
        fields = '__all__'


class EnablerTrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnablerTrainer
        fields = '__all__'


class LearnerRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearnerRole
        fields = '__all__'
