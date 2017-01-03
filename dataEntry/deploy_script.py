from dataEntry import runentry
from api.models import *


# #Car loading
# # Car.objects.all().delete()
# runentry.loadCars('aspect_ratio.csv')
# runentry.loadCarTrieFile()
#
#
#
# #Loading Services New
#
# # ServiceDealerCatNew.objects.all().delete()
# runentry.loadServiceDealerCatNew('Servicing_Labour.txt')
# ServicingNew.objects.all().delete()
# runentry.exportServicesListNew()
# runentry.loadPriceFreqNew('Servicing_Parts.txt')
#
#
#
# #Loading cleaning and value added services
#
# # CleaningDealerName.objects.all().delete()
# # CleaningServiceCat.objects.all().delete()
# # CleaningCategoryServices.objects.all().delete()
# runentry.loadCleaning('Cleaning_VAS_all.txt')
#
# runentry.updateCars()
# # runentry.deleteUserCart()




##Loading Services old

# ServiceDealerCat.objects.all().delete()
# runentry.loadServiceDealerCat('Servicing_Labour.txt')
# Servicing.objects.all().delete()
# runentry.exportServicesList()
# runentry.loadPri#ceFreq('Servicing_Parts.txt')



# VASDealerName.objects.all().delete()
# VASServiceCat.objects.all().delete()
# VASCategoryServices.objects.all().delete()


##Loading windshield
# WindShieldCat.objects.all().delete()
# WindShieldServiceDetails.objects.all().delete()
# runentry.loadWindShielddata('wsdata.txt')

# runentry.loadServicing('Servicing_List.txt')#
# runentry.loadWheelServices('WheelServices.txt')
# runentry.loadWheelServiceProvider('WheelServices_provider.txt')
# runentry.loadTyreSale('TyreSales.txt')
# Coupon.objects.all().delete()
# runentry.loadCoupon('Coupon.txt')


# ------------------------- Website Revamp---------------------------
Vehicle.objects.all().delete()
Services.objects.all().delete()
runentry.loadVehicles('vehicle_data.csv');
runentry.loadService('service_data_2.txt');
