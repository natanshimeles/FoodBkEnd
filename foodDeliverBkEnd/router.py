from UserManagement.views import AllUsersViewSets
from Order.viewsets import AllOrderViewSets,PhoneNumberViewSets,EmailAddressViewSets, PastDeliveryList,CancelledViewSets,AllReportsViewSets,ReadReportsViewSets,UnReadReportsViewSets,DeliveredOrderViewSets
from rest_framework import routers

router = routers.DefaultRouter()
router.register('allusers', AllUsersViewSets)
router.register('allorders', AllOrderViewSets)
router.register('canceledorder',CancelledViewSets)

router.register('allreports', AllReportsViewSets)
router.register('unreadreports', UnReadReportsViewSets)
router.register('readreports',ReadReportsViewSets)
router.register('completedorder', DeliveredOrderViewSets)

router.register('allphoneno', PhoneNumberViewSets)
router.register('allemailaddress', EmailAddressViewSets)