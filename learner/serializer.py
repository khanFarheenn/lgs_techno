from rest_framework import serializers
from .models import *
from django.core.exceptions import MultipleObjectsReturned

from django.db import IntegrityError

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

# ***************************LearnerSerializer***********************************************



class LearnerSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=100, write_only=True)
    last_name = serializers.CharField(max_length=100, write_only=True)
    password = serializers.CharField(max_length=100, write_only=True)
    email = serializers.EmailField(write_only=True)
    mobile_no = serializers.CharField(max_length=15)  
    gender = serializers.CharField(max_length=10)
    date_of_birth = serializers.DateField()
    qualification = serializers.CharField(max_length=255, allow_blank=True, required=False)  
    enrolment_date = serializers.DateField()
    
    # Relational fields
    proposer = serializers.PrimaryKeyRelatedField(queryset=Request.objects.all(), allow_null=True)
    approval_status = serializers.PrimaryKeyRelatedField(queryset=ProposerStatus.objects.all(), allow_null=True)
    approval_date = serializers.DateField(allow_null=True, required=False)
    rejection_reason = serializers.CharField(max_length=500, allow_null=True, required=False)

    def create(self, validated_data):
        # Assign a default or arbitrary username (non-unique)
        # username = validated_data.get('username') or "user_" + str(validated_data.get('email'))  # Default username logic

        user_data = {
            'first_name': validated_data.pop('first_name'),
            'last_name': validated_data.pop('last_name'),
            'password': validated_data.pop('password'),
            'email': validated_data.pop('email'),
            # 'username': username  # Set a default or arbitrary username, not checked for uniqueness
        }

        # Ensure email is unique
        if User.objects.filter(email=user_data['email']).exists():
            raise serializers.ValidationError("A user with this email already exists.")

        try:
            # Check if the role exists, and create it if necessary
            role, created = Role.objects.get_or_create(name='LEARNER')
        except MultipleObjectsReturned:
            raise serializers.ValidationError("Something went wrong: multiple roles found.")
        except Exception as e:
            # Catching any other exception that might arise during role creation/fetching
            raise serializers.ValidationError(f"Error fetching or creating role: {str(e)}")

        # Ensure role is created successfully
        if role is None:
            raise serializers.ValidationError("Role could not be created or fetched.")

        # Create the user with the given email and non-unique username
        try:
            user = User.objects.create_user(**user_data)  
            user.role.add(role)  
            user.save()  
        except IntegrityError:
            raise serializers.ValidationError("User creation failed due to an integrity error.")

        # Create learner instance with the validated data (including mobile_no, qualification, etc.)
        learner = Learner.objects.create(user=user, **validated_data)
        return learner

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        email = user_data.get('email')

        try:
            if email:
                user_instance = User.objects.get(email=email)
                instance.user.email = email

            instance.user.first_name = validated_data.get('first_name', instance.user.first_name)
            instance.user.last_name = validated_data.get('last_name', instance.user.last_name)

            instance.user.set_password(validated_data.get('password'))
            instance.user.email = validated_data.get('email', instance.user.email)
            instance.user.mobile_no = validated_data.get('mobile_no', instance.user.mobile_no)
            instance.gender = validated_data.get('gender', instance.gender)
            instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
            instance.qualification = validated_data.get('qualification', instance.qualification)
            instance.enrolment_date = validated_data.get('enrolment_date', instance.enrolment_date)
            instance.proposer = validated_data.get('proposer', instance.proposer)
            instance.approval_status = validated_data.get('approval_status', instance.approval_status)
            instance.approval_date = validated_data.get('approval_date', instance.approval_date)
            instance.rejection_reason = validated_data.get('rejection_reason', instance.rejection_reason)

            instance.user.save()
            instance.save()

            return instance
        except User.DoesNotExist:
            raise serializers.ValidationError("User with provided email does not exist.")
        except IntegrityError:
            raise serializers.ValidationError("User data could not be updated. Learner email already exists.")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.update({
            'first_name': instance.user.first_name,
            'last_name': instance.user.last_name,
            'email': instance.user.email,
            'mobile_no': instance.user.mobile_no,
            'gender': instance.gender,
            'date_of_birth': instance.date_of_birth,
            'qualification': instance.qualification,  
            'enrolment_date': instance.enrolment_date,
            'proposer': instance.proposer.id if instance.proposer else None,
            'approval_status': instance.approval_status.id if instance.approval_status else None,
            'approval_date': instance.approval_date,
            'rejection_reason': instance.rejection_reason,
        })
        return representation

    class Meta:
        model = Learner
        exclude = ['user']

# ***************************EnablerSerializer*******************************

# class EnablerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Enabler
#         fields = '__all__'




class EnablerSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=100, write_only=True)
    last_name = serializers.CharField(max_length=100, write_only=True)
    password = serializers.CharField(max_length=100, write_only=True)
    email = serializers.EmailField(write_only=True)
    mobile_no = serializers.CharField(max_length=15)
    enabler_type = serializers.ChoiceField(choices=[('Sponsor', 'Sponsor'), ('Trainer', 'Trainer')])
    description = serializers.CharField(max_length=1000)

    def create(self, validated_data):
        # Assign a default or arbitrary username (non-unique)
        # username = validated_data.get('username') or "user_" + str(validated_data.get('email'))  # Default username logic

        user_data = {
            'first_name': validated_data.pop('first_name'),
            'last_name': validated_data.pop('last_name'),
            'password': validated_data.pop('password'),
            'email': validated_data.pop('email'),
            # 'username': username  # Set a default or arbitrary username, not checked for uniqueness
        }

        # Ensure email is unique
        if User.objects.filter(email=user_data['email']).exists():
            raise serializers.ValidationError("A user with this email already exists.")

        # Create the user with the given email and non-unique username
        user = User.objects.create_user(**user_data)  # Create user with email and non-unique username
        user.save()  # Save the user

        # Create enabler instance
        enabler = Enabler.objects.create(user=user, **validated_data)
        return enabler

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        email = user_data.get('email')

        try:
            if email:
                user_instance = User.objects.get(email=email)
                instance.user.email = email

            instance.user.first_name = validated_data.get('first_name', instance.user.first_name)
            instance.user.last_name = validated_data.get('last_name', instance.user.last_name)

            instance.user.set_password(validated_data.get('password'))
            instance.user.email = validated_data.get('email', instance.user.email)
            instance.user.mobile_no = validated_data.get('mobile_no', instance.user.mobile_no)
            instance.enabler_type = validated_data.get('enabler_type', instance.enabler_type)
            instance.description = validated_data.get('description', instance.description)

            instance.user.save()
            instance.save()

            return instance
        except User.DoesNotExist:
            raise serializers.ValidationError("User with provided email does not exist.")
        except IntegrityError:
            raise serializers.ValidationError("User data could not be updated. Enabler email already exists.")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.update({
            'first_name': instance.user.first_name,
            'last_name': instance.user.last_name,
            'email': instance.user.email,
            'mobile_no': instance.user.mobile_no,
            'enabler_type': instance.enabler_type,
            'description': instance.description,
        })
        return representation

    class Meta:
        model = Enabler
        exclude = ['user']


# ****************************************SponsorSerializer*************************************

# class SponsorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Sponsor
#         fields = '__all__'



class SponsorSerializer(serializers.ModelSerializer):
    requestor = serializers.PrimaryKeyRelatedField(queryset=Request.objects.all())
    company_name = serializers.CharField(max_length=255)
    contribution_type = serializers.CharField(max_length=20)
    contribution_value = serializers.DecimalField(max_digits=10, decimal_places=2)
    contribution_details = serializers.CharField(max_length=1000)
    contribution_date = serializers.DateField()

    def create(self, validated_data):
        sponsor = Sponsor.objects.create(**validated_data)
        return sponsor

    def update(self, instance, validated_data):
        instance.company_name = validated_data.get('company_name', instance.company_name)
        instance.contribution_type = validated_data.get('contribution_type', instance.contribution_type)
        instance.contribution_value = validated_data.get('contribution_value', instance.contribution_value)
        instance.contribution_details = validated_data.get('contribution_details', instance.contribution_details)
        instance.contribution_date = validated_data.get('contribution_date', instance.contribution_date)

        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.update({
            'requestor': instance.requestor.id if instance.requestor else None,
            'company_name': instance.company_name,
            'contribution_type': instance.contribution_type,
            'contribution_value': instance.contribution_value,
            'contribution_details': instance.contribution_details,
            'contribution_date': instance.contribution_date,
        })
        return representation

    class Meta:
        model = Sponsor
        fields = '__all__'

# ********************************TrainerSerializer***********************************************

# class TrainerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Trainer
#         fields = '__all__'


class TrainerSerializer(serializers.ModelSerializer):
    request = serializers.PrimaryKeyRelatedField(queryset=Request.objects.all())
    job_title = serializers.CharField(max_length=100)
    job_description = serializers.CharField(max_length=1000)
    required_skills = serializers.CharField(max_length=1000)
    location = serializers.CharField(max_length=100)
    posting_date = serializers.DateField()
    application_deadline = serializers.DateField()
    experience = serializers.IntegerField(default=0)
    languages = serializers.CharField(max_length=255, allow_blank=True, required=False)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, allow_null=True, required=False)
    feedback = serializers.CharField(max_length=1000, allow_blank=True, required=False)

    def create(self, validated_data):
        trainer = Trainer.objects.create(**validated_data)
        return trainer

    def update(self, instance, validated_data):
        instance.job_title = validated_data.get('job_title', instance.job_title)
        instance.job_description = validated_data.get('job_description', instance.job_description)
        instance.required_skills = validated_data.get('required_skills', instance.required_skills)
        instance.location = validated_data.get('location', instance.location)
        instance.posting_date = validated_data.get('posting_date', instance.posting_date)
        instance.application_deadline = validated_data.get('application_deadline', instance.application_deadline)
        instance.experience = validated_data.get('experience', instance.experience)
        instance.languages = validated_data.get('languages', instance.languages)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.feedback = validated_data.get('feedback', instance.feedback)

        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.update({
            'request': instance.request.id if instance.request else None,
            'job_title': instance.job_title,
            'job_description': instance.job_description,
            'required_skills': instance.required_skills,
            'location': instance.location,
            'posting_date': instance.posting_date,
            'application_deadline': instance.application_deadline,
            'experience': instance.experience,
            'languages': instance.languages,
            'rating': instance.rating,
            'feedback': instance.feedback,
        })
        return representation

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
