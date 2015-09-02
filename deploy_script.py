from dataEntry import runentry
from api.models import *
runentry.loadCars('aspect_ratio.csv')
runentry.loadServicing('Servicing_List.txt')
runentry.loadServiceDealerCat('Servicing_Labour.txt')

#runentry.loadPriceFreq('Servicing_Parts.txt')


#runentry.loadWheelServices('WheelServices.txt')
#runentry.loadWheelServiceProvider('WheelServices_provider.txt')
#runentry.loadTyreSale('TyreSales.txt')