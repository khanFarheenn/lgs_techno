from django.contrib import admin
from .models import*

admin.site.register([IdType,Country,Address,City,State,Program,ProgramParticipant,
                     Request,ProposerStatus,BatchStatus,Sponsor,Learner,Trainer,
                     Enabler,Batch,BatchLearner,Assignment,JobApplication,JobReadiness,
                     EnablerSponsor,EnablerTrainer,LearnerRole])
