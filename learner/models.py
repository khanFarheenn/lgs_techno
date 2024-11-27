from django.db import models
from authentication.models import *



# IdType Model
class IdType(models.Model):
    idTypeName = models.CharField(max_length=100, unique=True)
    identity = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.idTypeName


# Country Model
class Country(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# State Model (linked to Country)
class State(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, related_name='states', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# City Model (linked to State)
class City(models.Model):
    name = models.CharField(max_length=255)
    state = models.ForeignKey(State, related_name='cities', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# Address Model
class Address(models.Model):
    address_line = models.CharField(max_length=255)
    city = models.ForeignKey(City, related_name='addresses', on_delete=models.CASCADE)
    postal_code = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.address_line}, {self.city.name}'


# Program Model
class Program(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.CharField(max_length=100)
    fee = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


# ProgramParticipants Model (Many-to-Many relationship between users and programs)
class ProgramParticipant(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.program

# Request Model
class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_sponsor = models.BooleanField(default=False)
    is_trainer = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email


# Proposer Status Model
class ProposerStatus(models.Model):
    name = models.CharField(max_length=250)
    step = models.IntegerField()

    def __str__(self):
        return self.name


# Learner Model
class Learner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    mobile_no = models.CharField(max_length=15, blank=True, null=True)
    qualification = models.CharField(max_length=255, blank=True, null=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    enrolment_date = models.DateField()
    proposer = models.ForeignKey(Request, on_delete=models.SET_NULL, null=True)
    approval_status = models.ForeignKey(ProposerStatus, on_delete=models.SET_NULL, null=True)
    approval_date = models.DateField(null=True, blank=True)
    rejection_reason = models.TextField(null=True, blank=True)
    id_type = models.ForeignKey(IdType, on_delete=models.CASCADE, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    subrole = models.ForeignKey(SubRole, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Learner: {self.user.email}"

# Enabler Model
class Enabler(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    enabler_type = models.CharField(max_length=50, choices=[('Sponsor', 'Sponsor'), ('Trainer', 'Trainer')])
    description = models.TextField()
    
    def __str__(self):
        return self.user.email
    
    
    
# Sponsor Model
class Sponsor(models.Model):
    requestor = models.ForeignKey(Request, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    contribution_type = models.CharField(max_length=20)
    contribution_value = models.DecimalField(max_digits=10, decimal_places=2)
    contribution_details = models.TextField()
    contribution_date = models.DateField()

    def __str__(self):
        return f"Sponsor - {self.requestor.user.username}"


# Trainer Model
class Trainer(models.Model):
    request = models.ForeignKey(Request, related_name='trainers', on_delete=models.CASCADE)
    job_title = models.CharField(max_length=100)
    job_description = models.TextField()
    required_skills = models.TextField()
    location = models.CharField(max_length=100)
    posting_date = models.DateField()
    application_deadline = models.DateField()
    experience = models.IntegerField(default=0)
    languages = models.CharField(max_length=255, blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.job_title
    


# BatchStatus Model
class BatchStatus(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name


# Batch Model
class Batch(models.Model):
    batch_id = models.CharField(max_length=50, unique=True)
    batch_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    capacity = models.IntegerField()
    status = models.ForeignKey(BatchStatus, on_delete=models.CASCADE)
    time_slot = models.CharField(max_length=100)

    def __str__(self):
        return self.batch_name


# BatchLearners Model (Many-to-Many relationship between learners and batches)
class BatchLearner(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE)

    def __str__(self):
        return self.batch_name




# Assignments Model
class Assignment(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    submission_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50)
    grade = models.CharField(max_length=10)
    
    def __str__(self):
        return self.learner


# JobReadiness Model
class JobReadiness(models.Model):
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE)
    is_ready_for_job = models.BooleanField(default=False)
    readiness_date = models.DateField()
    notes = models.TextField()
    
    def __str__(self):
        return self.learner


# JobApplication Model
class JobApplication(models.Model):
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    application_date = models.DateField()
    status = models.CharField(max_length=50)
    interview_date = models.DateField(null=True, blank=True)
    offer_date = models.DateField(null=True, blank=True)
    rejection_reason = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.learner




# EnablerSponsors Model (Many-to-Many between Enabler and Sponsor)
class EnablerSponsor(models.Model):
    enabler = models.ForeignKey(Enabler, on_delete=models.CASCADE)
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE)
    def __str__(self):
        return self.enabler


# EnablerTrainers Model (Many-to-Many between Enabler and Trainer)
class EnablerTrainer(models.Model):
    enabler = models.ForeignKey(Enabler, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    def __str__(self):
        return self.trainer


# LearnerRoles Model
class LearnerRole(models.Model):
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return self.learner