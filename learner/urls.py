from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *



router = DefaultRouter()


router.register(r'learners', LearnerView)
router.register(r'sponsers', SponsorView)
router.register(r'trainers', TrainerView)
router.register(r'enablers', EnablerView)
router.register(r'idtypes', IdTypeView)
router.register(r'countries', CountryView)
router.register(r'states', StateView)
router.register(r'cities', CityView)
router.register(r'addresses', AddressView)
router.register(r'programs', ProgramView)
router.register(r'programparticipants', ProgramParticipantView)
router.register(r'requests', RequestView)
router.register(r'proposerstatuses', ProposerStatusView)
router.register(r'batchstatuses', BatchStatusView)
router.register(r'batches', BatchView)
router.register(r'assignments', AssignmentView)
router.register(r'jobreadiness', JobReadinessView)
router.register(r'jobapplications', JobApplicationView)
router.register(r'enablersponsors', EnablerSponsorView)
router.register(r'enablertrainers', EnablerTrainerView)
router.register(r'learnerroles', LearnerRoleView)




urlpatterns = [
  

    path('', include(router.urls)),  
]
