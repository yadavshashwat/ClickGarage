__author__ = 'aragorn'

import os
import csv
import re
import json
from django.db.models.base import ObjectDoesNotExist


from activity.models import Transactions, CGUser
from api.models import *

# carMakers = ['Chevrolet', 'Datsun', 'Fiat', 'Ford', 'Honda', 'Hyundai', 'Mahindra', 'Maruti', 'Nissan', 'Skoda', 'Tata', 'Toyota', 'Volkswagen', 'Audi', 'Ssangyong', 'Maserati', 'Porsche', 'Mercedes-Benz', 'Rolls-Royce', 'Isuzu', 'Land', 'Mitsubishi', 'BMW', 'Lamborghini', 'Jaguar', 'Aston', 'Volvo', 'Ferrari', 'Mini', 'Bentley', 'Bugatti'];

carMakers = ['Maruti Suzuki','Hyundai', 'Honda', 'Toyota','Mahindra','Tata','Ford','Chevrolet','Renault','Volkswagen','Ashok Leyland','Aston Martin','Audi','Bentley','BMW','Bugatti','Caterham','Conquest','Datsun','DC','Ferrari','Fiat','Force','ICML','Isuzu','Jaguar','Koenigsegg','Lamborghini','Land Rover','Ssangyong','Maserati','Mercedes-Benz','Mini','Mitsubishi','Nissan','Porsche','Premier','Rolls-Royce','Skoda','Volvo','Royal Enfield','KTM','Honda','Suzuki','TVS','Bajaj','Yamaha','Hero']

path = os.path.dirname(os.path.realpath(__file__))
print path

def cleanstring(query):
    query = query.strip()
    query = re.sub('\s{2,}', ' ', query)
    query = re.sub(r'^"|"$', '', query)
    return query

def loadAspectRatio(fileName):
    with open(path+'/data/'+fileName, 'rU') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            print row[0]
            print row[1]
            # print ', '.join(row)

def loadCarTrieFile():
    carObjArray = Car.objects.all()
    carNameArray = []
    carTrieArgs = {}
    print 'running car trie load'
    for car in carObjArray :
        cname = car.make + ' ' + car.name
        # print cname
        if cname != None and cname not in carNameArray:
            carNameArray.append(cname)
    for name in carNameArray:
        nameArr = name.split(' ')
        for word in nameArr:
            if word.lower() in carTrieArgs:
                carTrieArgs[word.lower()].append(name)
            else:
                carTrieArgs[word.lower()] = [name]
    with open(path+'/carTrie.py', 'w') as carTrieFile:
        carTrieFile.write('carsTrie = '+json.dumps(carTrieArgs))
        carTrieFile.close()
    return carTrieArgs

def loadCars(fileName):
    with open(path+'/data/'+fileName, 'rU') as csvfile:
        carData = csv.reader(csvfile, delimiter=',', quotechar='|')
        for car in carData:
            carCompoundName = cleanstring(car[0])
            makeFound = False
            length = 1
            while not makeFound:
                make = " ".join(carCompoundName.split(' ')[:length])
                name_model = " ".join(carCompoundName.split(' ')[length:])
                if make in carMakers:
                    makeFound = True
                elif length > 2:
                    make = ''
                    name_model = carCompoundName
                    makeFound = True
                length = length+1

            aspectRatio = car[1]
            size = car[4]
            car_bike = car[2]
            cleaning_cat = car[3]
            # make = carCompoundName.split(' ')[0]
            # if make not in carMakers:
            #     make = ''
            #     name_model = carCompoundName
            # else:
            #     name_model = carCompoundName.split(' ', 1)[1]

            findCar = Car.objects.filter(name=name_model, make=make)
            if len(findCar):
                findCar = findCar[0]
                findCar.aspect_ratio = aspectRatio
                findCar.size = size
                findCar.car_bike = car_bike
                findCar.cleaning_cat = cleaning_cat
                findCar.save()
            else:
                cc = Car(make=make, name=name_model, year=0, aspect_ratio=aspectRatio, size = size, car_bike=car_bike, cleaning_cat = cleaning_cat)
                cc.save()


def updateCars():
    carObj = Car.objects.all()
    for c in carObj:
        car_name = c.name
        car_make = c.make
        complete_name = car_make + " " + car_name
        c.complete_vehicle_name = complete_name
        c.save()

def loadServicing(fileName):
    with open(path+'/data/Servicing/'+fileName, 'rU') as csvfile:
        carData = csv.reader(csvfile, delimiter='\t', quotechar='|')
        for car in carData:
            brand          = cleanstring(car[0])
            carname        = cleanstring(car[1])
            odometer       = cleanstring(car[2])
            year           = cleanstring(car[3])
            regular_checks = cleanstring(car[4]).split("$")
            findService = Servicing.objects.filter(brand=brand, carname=carname, odometer=odometer, year = year)
            if len(findService):
                findService = findService[0]
                findService.brand          = brand
                findService.carname        = carname
                findService.odometer       = odometer
                findService.year           = year
                findService.regular_checks = [regular_checks]
                findService.save()
            else:
                cc = Servicing(brand          = brand
                               ,carname        = carname
                               ,odometer       = odometer
                               ,year           = year
                               ,regular_checks = [regular_checks])
                cc.save()


def loadServiceDealerCat(fileName):
    with open(path+'/data/Servicing/'+fileName, 'rU') as csvfile:
        dealerData = csv.reader(csvfile, delimiter='\t', quotechar='|')
        for dealerz in dealerData:
            brand              = cleanstring(dealerz[0])
            carname            = cleanstring(dealerz[1])
            odometer           = cleanstring(dealerz[2])
            year               = cleanstring(dealerz[3])
            dealer_category    = cleanstring(dealerz[4])
            price_labour       = cleanstring(dealerz[5])
            wheel_alignment    = cleanstring(dealerz[6])
            wheel_balancing    = cleanstring(dealerz[7])
            WA_WB_Inc          = dealerz[8]
            regular_checks     = cleanstring(dealerz[9]).split("$")

            findDealer = ServiceDealerCat.objects.filter(brand = brand, carname=carname, dealer_category=dealer_category, odometer=odometer)
            if len(findDealer):
                findDealer = findDealer[0]
                findDealer.year              =  year
                findDealer.price_labour      =  price_labour
                findDealer.wheel_alignment   =  wheel_alignment
                findDealer.wheel_balancing   =  wheel_balancing
                findDealer.WA_WB_Inc         =  WA_WB_Inc
                findDealer.price_parts       =  "0"
                findDealer.regular_checks    = regular_checks
                findDealer.part_replacement  = []
                if (price_labour == "0"):
                    findDealer.paid_free = "Free"
                else:
                    findDealer.paid_free = "Paid"
                findDealer.save()
            else:
                if (price_labour == "0"):
                    paid_free = "Free"
                else:
                    paid_free = "Paid"
                cc = ServiceDealerCat(brand             =  brand
                                      ,carname           =  carname
                                      ,odometer          =  odometer
                                      ,dealer_category   =  dealer_category
                                      ,year              =  year
                                      ,price_labour      =  price_labour
                                      ,wheel_alignment   =  wheel_alignment
                                      ,wheel_balancing   =  wheel_balancing
                                      ,WA_WB_Inc         =  WA_WB_Inc
                                      ,price_parts = "0"
                                      ,part_replacement  = []
                                      ,regular_checks = regular_checks
                                      ,paid_free =  paid_free)
                cc.save()







                #Concatenating adding list of dealer to service data as well as paid/Free info - Shashwat

                #findService = Servicing.objects.filter(brand=brand, carname=carname, odometer=odometer)
                #if len(findService):
                #    findService = findService[0]
                #    dealers = findService.dealer
                #    dealers.append(dealer_category)
                #    findService.dealer = dealers
            #
            #    paid_free = findService.paid_free
            #    if price_labour == "0":
            #        paid_free = "Free"
            #    else:
            #        paid_free = "Paid"
            #    findService.paid_free = paid_free
            #    findService.save()


def exportServicesList():
    allServices = ServiceDealerCat.objects.all()
    p_f = ""
    for service in allServices:
        findDealer = Servicing.objects.filter(brand = service.brand, carname=service.carname, odometer=service.odometer)
        if len(findDealer):
            findDealer = findDealer[0]
            dealerz = findDealer.dealer
            dealerz.append(service.dealer_category)
            findDealer.dealer = dealerz
            if service.dealer_category == "Authorized":
                p_f = service.paid_free
            findDealer.paid_free = p_f
            findDealer.save()
        else:
            if service.dealer_category == "Authorized":
                p_f = service.paid_free

            cc = Servicing(brand                = service.brand
                           ,carname          = service.carname
                           ,odometer         = service.odometer
                           ,year             = service.year
                           ,regular_checks   = service.regular_checks
                           ,paid_free        = p_f
                           ,dealer           = [service.dealer_category])
            cc.save()



def loadPriceFreq(fileName):
    with open(path+'/data/Servicing/'+fileName, 'rU') as csvfile:
        partData = csv.reader(csvfile, delimiter='\t', quotechar='|')
        count = 0
        for prt in partData:
            count = count + 1
            print count
            brand            = cleanstring(prt[0])
            carname          = cleanstring(prt[1])
            part             = cleanstring(prt[2])
            freq             = int(cleanstring(prt[3]))
            first_occ        = int(cleanstring(prt[4]))
            second_occ       = int(cleanstring(prt[5]))
            dealer_category  = cleanstring(prt[6])
            unit             = cleanstring(prt[7])
            unit_price       = cleanstring(prt[8])
            net_price        = float(cleanstring(prt[9]))

            #print prt
            findDealer = ServiceDealerCat.objects.filter(brand = brand, carname=carname, dealer_category=dealer_category, odometer=str(first_occ))
            if len(findDealer):
                findDealer = findDealer[0]
                parts      = findDealer.part_replacement
                parts.append(part)
                findDealer.part_replacement = parts

                price_s = findDealer.price_parts
                price = float(price_s)
                price = price + net_price
                findDealer.price_parts = str(price)
                findDealer.save()


            findDealer = ServiceDealerCat.objects.filter(brand = brand, carname=carname, dealer_category=dealer_category, odometer=str(second_occ))
            if len(findDealer):
                findDealer = findDealer[0]
                parts = findDealer.part_replacement
                parts.append(part)
                findDealer.part_replacement = parts
                price_s = findDealer.price_parts
                price = float(price_s)
                price = price + net_price
                findDealer.price_parts = str(price)
                findDealer.save()

            odo = 0
            odo = second_occ + freq
            while (odo < 190000):
                findDealer = ServiceDealerCat.objects.filter(brand = brand, carname=carname, dealer_category=dealer_category, odometer=str(odo))
                if len(findDealer):
                    findDealer = findDealer[0]
                    parts = findDealer.part_replacement
                    parts.append(part)
                    findDealer.part_replacement = parts
                    price_s = findDealer.price_parts
                    price = float(price_s)
                    price = price + net_price
                    findDealer.price_parts = str(price)
                    findDealer.save()
                odo = odo + freq

    exportPartsList()

def exportPartsList():
    allServices = Servicing.objects.all()
    for service in allServices:
        findDealer = ServiceDealerCat.objects.filter(brand = service.brand, carname=service.carname, odometer=service.odometer)
        if len(findDealer):
            findDealer = findDealer[0]
            #print findDealer.part_replacement
            if findDealer.part_replacement == []:
                findDealer.part_replacement = ["No part replaced"]
                findDealer.save()
            service.part_replacement = findDealer.part_replacement
            service.save()

def loadCleaning(fileName):
    with open(path+'/data/Cleaning_VAS/'+fileName, 'rU') as csvfile:
        serviceData = csv.reader(csvfile, delimiter='\t', quotechar='|')
        for service_name in serviceData:
            vendor           = cleanstring(service_name[0])
            sup_cat          = cleanstring(service_name[1])
            service          = cleanstring(service_name[2])
            category         = cleanstring(service_name[3])
            car_cat          = cleanstring(service_name[4])
            price_labour     = cleanstring(service_name[5])
            price_parts      = cleanstring(service_name[6])
            price_total      = cleanstring(service_name[7])
            description      = cleanstring(service_name[8])
            doorstep         = cleanstring(service_name[9])
            discount         = cleanstring(service_name[10])
            car_bike         = cleanstring(service_name[11])
            priority         = cleanstring(service_name[12])
            # print priority
            if sup_cat == "Cleaning":
                findVendor = CleaningDealerName.objects.filter(vendor=vendor)
                if len(findVendor):
                    findVendor = findVendor[0]
                    findVendor.vendor          = vendor
                    findVendor.save()
                else:
                    cc = CleaningDealerName(vendor=vendor)
                    cc.save()

                findCatname = CleaningCatName.objects.filter(category=category, car_bike = car_bike)

                if len(findCatname):
                    findCatname = findCatname[0]
                    findCatname.category         = category
                    findCatname.car_bike = car_bike
                    findCatname.save()
                else:
                    ccat = CleaningCatName(category=category, car_bike = car_bike)
                    ccat.save()

                findCat = CleaningServiceCat.objects.filter(vendor=vendor,category = category, car_bike = car_bike)
                if len(findCat):
                    findCat = findCat[0]
                    findCat.vendor  = vendor
                    findCat.category = category
                    findCat.car_bike = car_bike
                    findCat.save()
                else:
                    clseca = CleaningServiceCat(vendor=vendor,category = category, car_bike = car_bike)
                    clseca.save()

                findService = CleaningCategoryServices.objects.filter(vendor=vendor,car_cat = car_cat,category = category,service=service, car_bike = car_bike)
                if len(findService):
                    findService = findService[0]
                    findService.price_labour     = price_labour
                    findService.price_parts      = price_parts
                    findService.price_total      = price_total
                    findService.description      = description
                    findService.doorstep         = doorstep
                    findService.discount         = discount
                    findService.priority        = priority
                    # print findService.priority
                    findService.save()
                else:
                    clcase = CleaningCategoryServices(vendor           = vendor
                                                      ,category         = category
                                                      ,car_cat          = car_cat
                                                      ,service          = service
                                                      ,price_labour     = price_labour
                                                      ,price_parts      = price_parts
                                                      ,price_total      = price_total
                                                      ,description      = description
                                                      ,doorstep         = doorstep
                                                      ,discount         = discount
                                                      ,priority        = priority
                                                      ,car_bike = car_bike   )
                    clcase.save()

            if sup_cat == "VAS":
                findVendor = VASDealerName.objects.filter(vendor=vendor)
                if len(findVendor):
                    findVendor = findVendor[0]
                    findVendor.vendor          = vendor
                    findVendor.save()
                else:
                    va = VASDealerName(vendor=vendor)
                    va.save()

                findCatname = VASCatName.objects.filter(category=category, car_bike = car_bike)

                if len(findCatname):
                    findCatname = findCatname[0]
                    findCatname.category         = category
                    findCatname.car_bike = car_bike
                    findCatname.save()
                else:
                    vcat = VASCatName(category=category, car_bike = car_bike)
                    vcat.save()



                findCat = VASServiceCat.objects.filter(vendor=vendor,category = category, car_bike = car_bike)
                if len(findCat):
                    findCat = findCat[0]
                    findCat.vendor  = vendor
                    findCat.category = category
                    findCat.car_bike = car_bike
                    findCat.save()
                else:
                    vaseca = VASServiceCat(vendor=vendor,category = category, car_bike = car_bike)
                    vaseca.save()

                findService = VASCategoryServices.objects.filter(vendor=vendor,car_cat = car_cat,category = category,service=service, car_bike = car_bike)
                if len(findService):
                    findService = findService[0]
                    findService.price_labour     = price_labour
                    findService.price_parts      = price_parts
                    findService.price_total      = price_total
                    findService.description      = description
                    findService.doorstep         = doorstep
                    findService.discount         = discount
                    findService.priority        = priority
                    findService.save()
                else:
                    vacase = VASCategoryServices(vendor           = vendor
                                                 ,category         = category
                                                 ,car_cat          = car_cat
                                                 ,service          = service
                                                 ,price_labour     = price_labour
                                                 ,price_parts      = price_parts
                                                 ,price_total      = price_total
                                                 ,description      = description
                                                 ,doorstep = doorstep
                                                 ,discount         = discount
                                                 ,car_bike = car_bike
                                                 ,priority        = priority )
                    vacase.save()

def loadServiceDealerName(fileName):
    with open(path+'/data/Servicing/'+fileName, 'rU') as csvfile:
        dealerData = csv.reader(csvfile, delimiter='\t', quotechar='|')
        for dealer in dealerData:
            name = dealer[0]
            make = dealer[1]
            dealer_category = dealer[2]
            address = dealer[3]
            phone = dealer[4]
            timing = dealer[5]
            findDealer = ServiceDealerName.objects.filter(name=name, make=make, dealer_category = dealer_category, address = address)
            if len(findDealer):
                findDealer = findDealer[0]
                findDealer.name = name
                findDealer.make = make
                findDealer.dealer_category= dealer_category
                findDealer.address = address
                findDealer.phone = phone
                findDealer.timing = timing
                findDealer.save()
            else:
                cc = ServiceDealerName(name=name, make = make,  dealer_category= dealer_category, address = address, phone = phone,timing = timing)
                cc.save()


def deleteUserCart():
    # obj = {}
    # obj['status'] = False
    # obj['message'] = 'Access Denied'
    # obj['result'] = []

    # if request.user.email in ['y.shashwat@gmail.com', 'shashwat@clickgarage.in', 'bhuvan.batra@gmail.com',
    #                           'sanskar@clickgarage.in', 'v.rajeev92@gmail.com', 'RajeevVempuluru']:
    userObjs = CGUser.objects.all()
    for user1 in userObjs:
        user1.uc_cart = ""
        user1.save()


def loadWindShielddata(fileName):
    with open(path+'/data/Windshield/'+fileName, 'rU') as csvfile:
        wsData = csv.reader(csvfile, delimiter='\t', quotechar='|')
        for ws in wsData:
            vendor          = cleanstring(ws[0])
            brand           = cleanstring(ws[1])
            carname         = cleanstring(ws[2])
            ws_type         = cleanstring(ws[3])
            ws_subtype      = cleanstring(ws[4])
            colour          = cleanstring(ws[5])
            price_ws        = cleanstring(ws[6])
            price_sealant   = cleanstring(ws[7])
            price_labour    = cleanstring(ws[8])
            price_total     = cleanstring(ws[9])
            city            = cleanstring(ws[10])
            price_insurance = cleanstring(ws[11])
            findWS = WindShieldServiceDetails.objects.filter(vendor = vendor, brand = brand, carname=carname, ws_type = ws_type, ws_subtype = ws_subtype, colour=colour, city=city)
            if len(findWS):
                findWS= findWS[0]
                findWS.vendor        = vendor
                findWS.brand         = brand
                findWS.carname       = carname
                findWS.ws_type       = ws_type
                findWS.ws_subtype    = ws_subtype
                findWS.colour  =colour
                findWS.price_ws      = price_ws
                findWS.price_sealant = price_sealant
                findWS.price_labour  = price_labour
                findWS.price_insurance   = price_insurance
                findWS.price_total = price_total
                findWS.city     = city
            else:
                cc = WindShieldServiceDetails(vendor        = vendor
                                              ,brand         = brand
                                              ,carname       = carname
                                              ,ws_type       = ws_type
                                              ,ws_subtype    = ws_subtype
                                              ,colour=colour
                                              ,price_ws      = price_ws
                                              ,price_sealant = price_sealant
                                              ,price_labour  = price_labour
                                              ,price_insurance   = price_insurance
                                              ,price_total = price_total
                                              ,city=city )
                cc.save()
    exportWindShieldCat()

def exportWindShieldCat():
    allServices = WindShieldServiceDetails.objects.all()
    for service in allServices:
        windshield = WindShieldCat.objects.filter(vendor=service.vendor,brand = service.brand, carname = service.carname, ws_type = service.ws_type)
        if len(windshield):
            windshield = windshield[0]
            windshield.save()
        else:
            cc = WindShieldCat(vendor=service.vendor,
                               brand=service.brand,
                               carname=service.carname,
                               ws_type=service.ws_type)
            cc.save()

def loadWheelServices(fileName):
    with open(path+'/data/WheelServices/'+fileName, 'rU') as csvfile:
        wheelData = csv.reader(csvfile, delimiter='\t', quotechar='|')
        for wheel in wheelData:
            service = wheel[0]
            description = wheel[1]
            findWheel = WheelServices.objects.filter(service=service)
            if len(findWheel):
                findWheel = findWheel[0]
                findWheel.service = service
                findWheel.description = description
                findWheel.save()
            else:
                cc = WheelServices(service = service,description = description)
                cc.save()

def loadWheelServiceProvider(fileName):
    with open(path+'/data/WheelServices/'+fileName, 'rU') as csvfile:
        wheelData = csv.reader(csvfile, delimiter='\t', quotechar='|')
        for wheel in wheelData:
            name    = wheel[0]
            address = wheel[1]
            phone   = wheel[2]
            timing  = wheel[3]
            car     = wheel[4]
            service = wheel[5]
            price   = wheel[6]
            findWheel   = WheelServiceProvider.objects.filter(name = name, address = address, car = car, service=service)
            if len(findWheel):
                findWheel = findWheel[0]
                findWheel.name     =  name
                findWheel.address  =  address
                findWheel.phone    =  phone
                findWheel.timing   =  timing
                findWheel.service  =  service
                findWheel.car      =  car
                findWheel.price    =  price
                findWheel.save()
            else:
                cc = WheelServiceProvider(name = name ,address = address, phone = phone, timing = timing , service = service,car =  car ,price = price  )
                cc.save()


def loadTyreSale(fileName):
    with open(path+'/data/WheelServices/'+fileName, 'rU') as csvfile:
        wheelData = csv.reader(csvfile, delimiter='\t', quotechar='|')
        for wheel in wheelData:
            name          = wheel[0]
            address       = wheel[1]
            aspect_key    = wheel[2]
            brand         = wheel[3]
            model         = wheel[4]
            width         = wheel[5]
            aspect_ratio  = wheel[6]
            rim_size      = wheel[7]
            load_rating   = wheel[8]
            speed_rating  = wheel[9]
            warranty      = wheel[10]
            price         = wheel[11]
            findWheel     = TyreSale.objects.filter(name = name, aspect_key = aspect_key, address = address, brand=brand, model=model  )
            if len(findWheel):
                findWheel = findWheel[0]
                findWheel.name          = name
                findWheel.address       = address
                findWheel.aspect_key    = aspect_key
                findWheel.brand         = brand
                findWheel.model         = model
                findWheel.width         = width
                findWheel.aspect_ratio  = aspect_ratio
                findWheel.rim_size      = rim_size
                findWheel.load_rating   = load_rating
                findWheel.speed_rating  = speed_rating
                findWheel.warranty      =  warranty
                findWheel.price         = price
                findWheel.save()
            else:
                cc = TyreSale(
                    name          = name ,
                    address       = address,
                    aspect_key    = aspect_key   ,
                    brand         = brand        ,
                    model         = model        ,
                    width         = width        ,
                    aspect_ratio  = aspect_ratio ,
                    rim_size      = rim_size     ,
                    load_rating   = load_rating  ,
                    speed_rating  = speed_rating ,
                    warranty      = warranty     ,
                    price         = price        )
                cc.save()
#                 print carCompundName.split(' ')[0]
#    print iceMake


#lloadAspectRatio('aspect_ratio.csv')

############################# Servicing New ##############################


def loadServiceDealerCatNew(fileName):
    with open(path+'/data/ServicingNew/'+fileName, 'rU') as csvfile:
        dealerData = csv.reader(csvfile, delimiter='\t', quotechar='|')
        for dealerz in dealerData:
            brand              = cleanstring(dealerz[0])
            carname            = cleanstring(dealerz[1])
            type_service       = cleanstring(dealerz[2])
            service_desc       = cleanstring(dealerz[3])
            dealer_category    = cleanstring(dealerz[4])
            price_labour       = cleanstring(dealerz[5])
            priority           = dealerz[6]
            discount           = dealerz[7]
            priority_service   = dealerz[8]
            car_bike           = cleanstring(dealerz[9])
            wheel_alignment    = cleanstring(dealerz[10])
            wheel_balancing    = cleanstring(dealerz[11])
            dry_cleaning       = cleanstring(dealerz[12])
            engine_additive    = cleanstring(dealerz[13])
            injector_cleaning  = cleanstring(dealerz[14])
            rubbing_polishing  = cleanstring(dealerz[15])
            anti_rust          = cleanstring(dealerz[16])
            teflon             = cleanstring(dealerz[17])
            engine_flush       =  cleanstring(dealerz[18])
            ac_servicing       = cleanstring(dealerz[19])
            ac_disinfection    = cleanstring(dealerz[20])

            # WA_WB_Inc          = dealerz[7]



            findDealer = ServiceDealerCatNew.objects.filter(brand = brand, carname=carname, dealer_category=dealer_category, type_service=type_service)
            if len(findDealer):
                findDealer = findDealer[0]
                # findDealer.year              =  year
                findDealer.price_labour      =  price_labour
                findDealer.wheel_alignment   =  wheel_alignment
                findDealer.wheel_balancing   =  wheel_balancing
                # findDealer.WA_WB_Inc         =  WA_WB_Inc
                findDealer.price_parts       =  "0"
                findDealer.service_desc      =  service_desc
                # findDealer.regular_checks    = regular_checks
                findDealer.discount    = discount
                findDealer.priority    = priority
                findDealer.priority_service = priority_service
                findDealer.car_bike     = car_bike
                findDealer.part_replacement  = []
                findDealer.part_dic =[]
                findDealer.detail_dealers = []
                findDealer.dry_cleaning        = dry_cleaning
                findDealer.engine_additive     = engine_additive
                findDealer.injector_cleaning   = injector_cleaning
                findDealer.rubbing_polishing   = rubbing_polishing
                findDealer.anti_rust           = anti_rust
                findDealer.teflon               = teflon
                findDealer.engine_flush        = engine_flush
                findDealer.ac_servicing        = ac_servicing
                findDealer.ac_disinfection     = ac_disinfection
                # obj = {}
                # obj['part_name']= part
                # obj['part_price']= minor_price
                # obj['part_action'] = minor_action
                # obj['units'] = minor_qty
                # obj['unit_price'] = unit_price
                #
                #
                # obj_list = findDealer.part_dic
                # obj_list.append(obj)



                # if (price_labour == "0"):
                #     findDealer.paid_free = "Free"
                # else:
                #     findDealer.paid_free = "Paid"
                findDealer.save()
            else:
                # if (price_labour == "0"):
                #     paid_free = "Free"
                # else:
                #     paid_free = "Paid"
                cc = ServiceDealerCatNew(brand             =  brand
                                         ,carname           =  carname
                                         ,type_service      =  type_service
                                         ,dealer_category   =  dealer_category
                                         ,service_desc      =  service_desc
                                         ,price_labour      =  price_labour
                                         ,wheel_alignment   =  wheel_alignment
                                         ,wheel_balancing   =  wheel_balancing
                                         # ,WA_WB_Inc         =  WA_WB_Inc
                                         ,price_parts = "0"
                                         ,part_replacement  = []
                                         # ,regular_checks = regular_checks
                                         ,part_dic = []
                                         ,detail_dealers = []
                                         ,discount    = discount
                                         ,priority    = priority
                                         ,car_bike = car_bike
                                         # ,paid_free =  paid_free
                                         ,priority_service = priority_service
                                         ,dry_cleaning        = dry_cleaning
                                         ,engine_additive     = engine_additive
                                         ,injector_cleaning   = injector_cleaning
                                         ,rubbing_polishing   = rubbing_polishing
                                         ,anti_rust           = anti_rust
                                         ,teflon               = teflon
                                         ,engine_flush        = engine_flush
                                         ,ac_servicing        = ac_servicing
                                         ,ac_disinfection     = ac_disinfection
                                         )
                cc.save()


                #Concatenating adding list of dealer to service data as well as paid/Free info - Shashwat

                #findService = Servicing.objects.filter(brand=brand, carname=carname, odometer=odometer)
                #if len(findService):
                #    findService = findService[0]
                #    dealers = findService.dealer
                #    dealers.append(dealer_category)
                #    findService.dealer = dealers
            #
            #    paid_free = findService.paid_free
            #    if price_labour == "0":
            #        paid_free = "Free"
            #    else:
            #        paid_free = "Paid"
            #    findService.paid_free = paid_free
            #    findService.save()

def exportServicesListNew():
    allServices = ServiceDealerCatNew.objects.all()
    # p_f = ""
    for service in allServices:
        findDealer = ServicingNew.objects.filter(brand = service.brand, carname=service.carname, type_service=service.type_service)
        if len(findDealer):
            findDealer = findDealer[0]
            dealerz = findDealer.dealer
            dealerz.append(service.dealer_category)
            findDealer.dealer = dealerz
            # if service.dealer_category == "Authorized":
            #     p_f = service.paid_free
            # findDealer.paid_free = p_f
            findDealer.save()
        else:
            # if service.dealer_category == "Authorized":
            #     p_f = service.paid_free

            cc = ServicingNew(brand             = service.brand
                              ,carname          = service.carname
                              ,type_service     =service.type_service
                              ,service_desc     = service.service_desc
                              ,priority_service =service.priority_service
                              # ,year             = service.year
                              ,regular_checks   = service.regular_checks
                              # ,paid_free        = p_f
                              ,dealer           = [service.dealer_category])
            cc.save()



def loadPriceFreqNew(fileName):
    with open(path+'/data/ServicingNew/'+fileName, 'rU') as csvfile:
        partData = csv.reader(csvfile, delimiter='\t', quotechar='|')
        count = 0
        for prt in partData:
            count = count + 1
            print count
            brand            = cleanstring(prt[0])
            carname          = cleanstring(prt[1])
            part             = cleanstring(prt[2])
            # minor            = int(cleanstring(prt[3]))
            # major            = int(cleanstring(prt[4]))
            #second_occ      = int(cleanstring(prt[5]))
            dealer_category  = cleanstring(prt[3])
            unit             = cleanstring(prt[4])
            unit_price       = cleanstring(prt[5])
            minor_qty      = cleanstring(prt[6])
            major_qty      = cleanstring(prt[7])
            minor_price      = float(cleanstring(prt[8]))
            major_price      = float(cleanstring(prt[9]))
            minor_action     = cleanstring(prt[10])
            major_action     = cleanstring(prt[11])
            check_action      = cleanstring(prt[12])
            # to_add      =  cleanstring(prt[13])


            service_1 = ""
            service_2 = ""
            service_3 = ""
            service_4 = ""
            service_5 = ""

            #
            service_1 = "Standard Service"
            service_2 ="Comprehensive Service"
            # service_3 = "Not Defined"
            # service_4 = "Regular"
            service_5 = "General Check Up"
            # if (major == 1):

            #print prt

            findDealer = ServiceDealerCatNew.objects.filter(brand = brand, carname=carname, dealer_category=dealer_category, type_service=service_1)
            if len(findDealer):
                findDealer = findDealer[0]
                parts      = findDealer.part_replacement
                parts.append(part)
                findDealer.part_replacement = parts

                price_s = findDealer.price_parts
                price = float(price_s)
                # if (to_add=="1"):
                price = price + minor_price
                findDealer.price_parts = str(price)

                obj = {}
                obj['part_name']= part
                obj['part_price']= minor_price
                obj['part_action'] = minor_action
                obj['units'] = minor_qty
                obj['unit_price'] = unit_price


                obj_list = findDealer.part_dic
                obj_list.append(obj)

                findDealer.save()

            findDealer = ServiceDealerCatNew.objects.filter(brand = brand, carname=carname, dealer_category=dealer_category, type_service=service_2)

            if len(findDealer):
                findDealer = findDealer[0]
                parts = findDealer.part_replacement
                parts.append(part)
                findDealer.part_replacement = parts
                price_s = findDealer.price_parts
                price = float(price_s)
                # if (to_add=="1"):
                price = price + major_price
                findDealer.price_parts = str(price)

                obj = {}
                obj['part_name']= part
                obj['part_price']= major_price
                obj['part_action'] = major_action
                obj['units'] = major_qty
                obj['unit_price'] = unit_price

                obj_list = findDealer.part_dic
                obj_list.append(obj)
                findDealer.part_dic = obj_list

                findDealer.save()

            findDealer = ServiceDealerCatNew.objects.filter(brand = brand, carname=carname, dealer_category=dealer_category, type_service=service_3)

            if len(findDealer):
                findDealer = findDealer[0]
                parts = findDealer.part_replacement
                parts.append(part)
                findDealer.part_replacement = parts
                price_s = findDealer.price_parts
                price = float(price_s)
                # if (to_add=="1"):
                price = price + minor_price
                findDealer.price_parts = str(price)

                obj = {}
                obj['part_name']= part
                obj['part_price']= minor_price
                obj['part_action'] = minor_action
                obj['units'] = minor_qty
                obj['unit_price'] = unit_price


                obj_list = findDealer.part_dic
                obj_list.append(obj)
                findDealer.part_dic = obj_list
                findDealer.save()


            findDealer = ServiceDealerCatNew.objects.filter(brand = brand, carname=carname, dealer_category=dealer_category, type_service=service_4)

            if len(findDealer):
                findDealer = findDealer[0]
                parts = findDealer.part_replacement
                parts.append(part)
                findDealer.part_replacement = parts
                price_s = findDealer.price_parts
                price = float(price_s)
                # if (to_add=="1"):
                price = price + minor_price

                findDealer.price_parts = str(price)

                obj = {}
                obj['part_name']= part
                obj['part_price']= minor_price
                obj['part_action'] = minor_action
                obj['units'] = minor_qty
                obj['unit_price'] = unit_price

                obj_list = findDealer.part_dic
                obj_list.append(obj)
                findDealer.part_dic = obj_list
                findDealer.save()

            findDealer = ServiceDealerCatNew.objects.filter(brand = brand, carname=carname, dealer_category=dealer_category, type_service=service_5)

            if len(findDealer):
                findDealer = findDealer[0]
                parts = findDealer.part_replacement
                parts.append(part)
                findDealer.part_replacement = parts
                price_s = findDealer.price_parts
                price = float(price_s)
                # if (to_add=="1"):
                #     price = price + minor_price

                findDealer.price_parts = 0

                obj = {}
                obj['part_name']= part
                obj['part_price']= "NA"
                obj['part_action'] = check_action
                obj['units'] = "NA"
                obj['unit_price'] = "NA"


                obj_list = findDealer.part_dic
                obj_list.append(obj)
                findDealer.part_dic = obj_list
                findDealer.save()

                # odo = 0
                # odo = second_occ + freq

                # while (odo < 190000):
                #     findDealer = ServiceDealerCat.objects.filter(brand = brand, carname=carname, dealer_category=dealer_category, odometer=str(odo))
                #     if len(findDealer):
                #         findDealer = findDealer[0]
                #         parts = findDealer.part_replacement
                #         parts.append(part)
                #         findDealer.part_replacement = parts
                #         price_s = findDealer.price_parts
                #         price = float(price_s)
                #         price = price + net_price
                #         findDealer.price_parts = str(price)
                #         findDealer.save()
                #     odo = odo + freq

    exportPartsListNew()

def exportPartsListNew():
    allServices = ServicingNew.objects.all()
    for service in allServices:
        findDealer = ServiceDealerCatNew.objects.filter(brand = service.brand, carname=service.carname, type_service=service.type_service)
        if len(findDealer):
            findDealer = findDealer[0]
            #print findDealer.part_replacement
            if findDealer.part_replacement == []:
                findDealer.part_replacement = ["No part replaced"]
                findDealer.save()
            service.part_replacement = findDealer.part_replacement
            # if findDealer.part_dic == []:
            #     findDealer.part_dic = ["No part replaced"]
            #     findDealer.save()
            service.part_dic = findDealer.part_dic
            service.save()

def loadDealerListNew(fileName):
    with open(path+'/data/ServicingNew/'+fileName, 'rU') as csvfile:
        dealerData = csv.reader(csvfile, delimiter='\t', quotechar='|')
        count = 0
        for dlr in dealerData:
            count = count + 1
            print count
            brand            = cleanstring(dlr[0])
            name             = cleanstring(dlr[1])
            city             = cleanstring(dlr[2])
            region           = cleanstring(dlr[3])
            offday           = cleanstring(dlr[4]).split("$")
            locality          = cleanstring(dlr[5])
            landline         = cleanstring(dlr[6])
            mobile           = cleanstring(dlr[7])
            car_bike         = cleanstring(dlr[8])
            address          = cleanstring(dlr[9])
            spc_address      = cleanstring(dlr[10])
            landmark         = cleanstring(dlr[11])
            pincode          = cleanstring(dlr[12])
            contact_prs      = cleanstring(dlr[13])
            status           = cleanstring(dlr[14])

            findCar = Car.objects.filter(make=brand, car_bike=car_bike)
            for crz in findCar:
                carname = crz.name
                carfinal = brand + " " + carname
                findService = ServiceDealerCatNew.objects.filter(carname=carfinal)
                for service in findService:
                    obj = {}
                    obj['name']= name
                    obj['city']= city
                    obj['region']= region
                    obj['offday']= offday
                    obj['address']= address
                    obj['locality'] = locality
                    obj['spc_address'] = spc_address
                    obj['landmark'] = landmark
                    obj['pincode'] = pincode
                    obj['cnt_prs'] = contact_prs
                    obj['status'] = status
                    obj['landline']= landline
                    obj['mobile']= mobile
                    obj_list = service.detail_dealers
                    obj_list.append(obj)
                    service.save()

def loadCoupon(fileName):
    with open(path+'/data/'+fileName, 'rU') as csvfile:
        couponData = csv.reader(csvfile, delimiter='\t', quotechar='|')
        for coupon in couponData:
            coupon_code      = cleanstring(coupon[0])
            date_issue       = cleanstring(coupon[1])
            valid_till_date  = cleanstring(coupon[2])
            discount         = cleanstring(coupon[3])
            cashback         = cleanstring(coupon[4])
            message          = cleanstring(coupon[5])
            valid            = cleanstring(coupon[6])
            category         = cleanstring(coupon[7])
            car_bike         = cleanstring(coupon[8])
            vendor           = cleanstring(coupon[9])

            findCoupon     = Coupon.objects.filter(coupon_code=coupon_code)
            if len(findCoupon):
                findCoupon = findCoupon[0]
                findCoupon.coupon_code      = coupon_code
                findCoupon.date_issue       = date_issue
                findCoupon.valid_till_date  = valid_till_date
                findCoupon.discount         = discount
                findCoupon.cashback         = cashback
                findCoupon.message          = message
                findCoupon.valid            = valid
                findCoupon.category  = category
                findCoupon.car_bike  = car_bike
                findCoupon.vendor    = vendor



                findCoupon.save()
            else:
                cc = Coupon(
                    coupon_code       =  coupon_code
                    ,date_issue       =  date_issue
                    ,valid_till_date  =  valid_till_date
                    ,discount         =  discount
                    ,cashback         =  cashback
                    ,message          =  message
                    ,valid            =  valid
                    ,category  = category
                    ,car_bike  = car_bike
                    ,vendor    = vendor
                )
                cc.save()



# ---------------------------------- Website Revamp ------------------------------------------

def loadVehicles(fileName):
    with open(path+'/data revamp/'+fileName, 'rU') as csvfile:
        vehicleData = csv.reader(csvfile, delimiter=',', quotechar='|')
        for vehicle in vehicleData:
            make                = cleanstring(vehicle[0])
            model               = cleanstring(vehicle[1])
            year                = cleanstring(vehicle[2])
            fuel_type           = cleanstring(vehicle[3])
            full_veh_name       = cleanstring(vehicle[4])
            aspect_ratio        = cleanstring(vehicle[5])
            type                = cleanstring(vehicle[6])
            car_bike            = cleanstring(vehicle[7])
            engine_oil          = cleanstring(vehicle[8])
            active              = cleanstring(vehicle[9])
            findVehicle = Vehicle.objects.filter(make=make,
                                                 model=model,
                                                 year=year,
                                                 fuel_type = fuel_type)
            if len(findVehicle):
                findVehicle = findVehicle[0]
                findVehicle.make          = make
                findVehicle.model         = model
                findVehicle.year          = year
                findVehicle.fuel_type     = fuel_type
                findVehicle.full_veh_name = full_veh_name
                findVehicle.aspect_ratio  = aspect_ratio
                findVehicle.type          = type
                findVehicle.car_bike      = car_bike
                findVehicle.engine_oil    = engine_oil
                findVehicle.active        = active
                findVehicle.save()
            else:
                veh = Vehicle(
                    make         = make         ,
                    model        = model        ,
                    year         = year         ,
                    fuel_type    = fuel_type    ,
                    full_veh_name= full_veh_name,
                    aspect_ratio = aspect_ratio ,
                    type         = type         ,
                    car_bike     = car_bike     ,
                    engine_oil   = engine_oil   ,
                    active       = active        )
                veh.save()

def loadService(fileName):
    with open(path+'/data revamp/'+fileName, 'rU') as csvfile:
        serviceData = csv.reader(csvfile, delimiter='\t', quotechar='|')
        for service in serviceData:
            make                = cleanstring(service[0])
            model               = cleanstring(service[1])
            year                = cleanstring(service[2])
            fuel_type           = cleanstring(service[3])
            full_veh_name       = cleanstring(service[4])
            car_bike            = cleanstring(service[5])
            city                = cleanstring(service[6])
            service_cat         = cleanstring(service[7])
            service_desc        = cleanstring(service[8])
            job_name            = cleanstring(service[9])
            doorstep            = cleanstring(service[10])
            dealer              = cleanstring(service[11])
            name                = cleanstring(service[12])
            type                = cleanstring(service[13])
            action              = cleanstring(service[14])
            quantity            = cleanstring(service[15])
            unit                = cleanstring(service[16])
            price               = cleanstring(service[17])
            brand               = cleanstring(service[18])
            price_comp          = cleanstring(service[19])
            job_summary         = cleanstring(service[20]).split("$")
            job_desc            = cleanstring(service[21])
            job_features        = cleanstring(service[22]).split("$")
            job_symptoms        = cleanstring(service[23]).split("$")
            priority            = cleanstring(service[24])
            time                = cleanstring(service[25])
            default             = cleanstring(service[26])
            # print(time)
            # print(make)


            findService = Services.objects.filter(
                make             = make             ,
                model            = model            ,
                year             = year             ,
                fuel_type        = fuel_type        ,
                full_veh_name    = full_veh_name    ,
                car_bike         = car_bike         ,
                city             = city             ,
                service_cat      = service_cat      ,
                job_name         = job_name         ,
                doorstep         = doorstep         ,
                dealer           = dealer)
            if len(findService):
                findService = findService[0]
                findService.make             = make
                findService.model            = model
                findService.year             = year
                findService.fuel_type        = fuel_type
                findService.full_veh_name    = full_veh_name
                findService.car_bike         = car_bike
                findService.city             = city
                findService.service_cat      = service_cat
                findService.service_desc     = service_desc
                findService.job_name         = job_name
                findService.job_desc         = job_desc
                findService.doorstep         = doorstep
                findService.dealer           = dealer
                # obj_default = []
                # obj_option = []
                obj = {}
                obj['name'] = name
                obj['action'] = action
                obj['quantity'] = quantity
                obj['unit'] = unit
                obj['type'] = type
                obj['price'] = price
                obj['brand'] = brand
                obj['price_comp'] = price_comp
                if default == "default":
                    findService.default_components.append(obj)
                    price_string = findService.total_price
                    price_float_t = float(price_string)
                    price_string_2 = findService.total_price_comp
                    price_float_2 = float(price_string_2)

                    price_string_p = findService.total_part
                    price_float_p = float(price_string_p)
                    price_string_l = findService.total_labour
                    price_float_l = float(price_string_l)
                    price_string_d = findService.total_discount
                    price_float_d = float(price_string_d)

                    if type == "Discount":
                        price_float_t = price_float_t - float(price)
                        price_float_2 = price_float_2 - float(price_comp)
                        price_float_d = price_float_d + float(price)
                    elif type == "Part":
                        price_float_t = price_float_t + float(price)
                        price_float_2 = price_float_2 + float(price_comp)
                        price_float_p = price_float_p + float(price)
                    elif type == "Labour":
                        price_float_t = price_float_t + float(price)
                        price_float_2 = price_float_2 + float(price_comp)
                        price_float_l = price_float_l + float(price)

                else:
                    findService.optional_components.append(obj)
                findService.total_price        = price_float_t
                findService.total_part        = price_float_p
                findService.total_labour        = price_float_l
                findService.total_discount        = price_float_d

                findService.total_price_comp   = price_float_2
                findService.priority         = priority
                findService.save()
            else:
                obj_default = []
                obj_option = []
                obj = {}
                obj['name'] = name
                obj['action'] = action
                obj['quantity'] = quantity
                obj['unit'] = unit
                obj['type'] = type
                obj['price'] = price
                obj['brand'] = brand
                obj['price_comp'] = price_comp

                price_float_t_3 = 0
                price_float_p_3 = 0
                price_float_l_3 = 0
                price_float_d_3 = 0
                price_float_4 = 0

                if default == "default":
                    obj_default.append(obj)
                    if type == "Discount":
                        price_float_t_3 = -1*float(price)
                        price_float_d_3 = float(price)
                        price_float_4 = -1*float(price_comp)
                    elif type == "Part":
                        price_float_t_3 = float(price)
                        price_float_p_3 = float(price)
                        price_float_4 = float(price_comp)
                    elif type == "Labour":
                        price_float_t_3 = float(price)
                        price_float_l_3 = float(price)
                        price_float_4 = float(price_comp)
                    else:
                        price_float_t_3 = 0
                        price_float_p_3 = 0
                        price_float_l_3 = 0
                        price_float_d_3 = 0

                else :
                    obj_option.append(obj)
                    price_float_t_3 = 0
                    price_float_4 = 0
                # price_string_3 = str(price_float_3)
                # price_string_4 = str(price_float_4)
                serv = Services(
                    make 			    = make,
                    model 				= model,
                    year 				= year,
                    fuel_type 			= fuel_type,
                    full_veh_name 		= full_veh_name,
                    car_bike 			= car_bike,
                    city 				= city,
                    service_cat			= service_cat,
                    service_desc        = service_desc,
                    job_name 	        = job_name,
                    doorstep            = doorstep,
                    job_summary         = job_summary,
                    job_desc            = job_desc,
                    job_features        = job_features,
                    job_symptoms        = job_symptoms,
                    dealer  			= dealer,
                    default_components  = obj_default,
                    optional_components = obj_option,
                    total_price         = price_float_t_3,
                    total_part          =price_float_p_3,
                    total_labour        =price_float_l_3,
                    total_discount      = price_float_d_3,
                    total_price_comp    = price_float_4,
                    priority            = priority,
                    time                = time
                )
                serv.save()

def loadServiceParts(fileName):
    with open(path+'/data revamp/'+fileName, 'rU') as csvfile:
        serviceData = csv.reader(csvfile, delimiter='\t', quotechar='|')
        for service in serviceData:
            city                = cleanstring(service[0])
            vendor              = cleanstring(service[1])
            make                = cleanstring(service[2])
            model               = cleanstring(service[3])
            year                = cleanstring(service[4])
            fuel_type           = cleanstring(service[5])
            full_veh_name       = cleanstring(service[6])
            type                = cleanstring(service[7])
            car_bike            = cleanstring(service[8])
            service_cat         = cleanstring(service[9])
            job_name            = cleanstring(service[10])
            doorstep            = cleanstring(service[11])
            part_name           = cleanstring(service[12])
            action              = cleanstring(service[13])
            quantity            = cleanstring(service[14])
            units               = cleanstring(service[15])
            price               = cleanstring(service[16])
            part_cat            = cleanstring(service[17])
            price_comp          = cleanstring(service[18])
            default             = cleanstring(service[19])

            findService = ServicePart.objects.filter(
                city             =city              ,
                vendor           =vendor            ,
                make             = make             ,
                model            = model            ,
                year             = year             ,
                fuel_type        = fuel_type        ,
                full_veh_name    = full_veh_name    ,
                type             = type             ,
                car_bike         = car_bike         ,
                service_cat      = service_cat      ,
                job_name         = job_name         ,
                doorstep         = doorstep
            )

            if len(findService):
                findService = findService[0]
                findService.city             = city
                findService.vendor           = vendor
                findService.make             = make
                findService.model            = model
                findService.year             = year
                findService.fuel_type        = fuel_type
                findService.full_veh_name    = full_veh_name
                findService.type             = type
                findService.car_bike         = car_bike
                findService.city             = city
                findService.service_cat      = service_cat
                findService.job_name         = job_name
                findService.doorstep         = doorstep
                obj = {}
                obj['name'] = part_name
                obj['action'] = action
                obj['quantity'] = quantity
                obj['unit_price'] = units
                obj['price'] = price
                obj['category'] = part_cat
                obj['price_comp'] = price_comp
                obj['type'] = "Part"
                obj['settlement_cat'] = "Part"

                # price_float_t = 0
                # price_float_c = 0
                # price_string = findService.total_price
                price_float_t = findService.total_price
                # price_string_2 = findService.total_price_comp
                price_float_c = findService.total_price_comp

                if default == "Default":

                    findService.default_components.append(obj)
                    price_float_t = price_float_t + float(price)
                    price_float_c = price_float_c + float(price_comp)

                else:
                    findService.optional_components.append(obj)
                    price_float_t = price_float_t
                    price_float_c = price_float_c

                findService.total_price        = price_float_t
                findService.total_price_comp   = price_float_c
                findService.save()
            else:
                obj_default = []
                obj_option = []
                obj = {}
                obj['name'] = part_name
                obj['action'] = action
                obj['quantity'] = quantity
                obj['unit_price'] = units
                obj['price'] = price
                obj['category'] = part_cat
                obj['price_comp'] = price_comp
                obj['type'] = "Part"
                obj['settlement_cat'] = "Part"

                price_float_t_2 = 0
                price_float_c_2 = 0

                if default == "Default":
                    obj_default.append(obj)
                    price_float_t_2 = float(price)
                    price_float_c_2 = float(price_comp)
                else:
                    obj_option.append(obj)
                    # price_float_t_2 = price_float_t_2
                    # price_float_c_2 = price_float_c_2

                serv = ServicePart(
                    city             =city              ,
                    vendor           =vendor            ,
                    make             = make             ,
                    model            = model            ,
                    year             = year             ,
                    fuel_type        = fuel_type        ,
                    full_veh_name    = full_veh_name    ,
                    type             = type             ,
                    car_bike         = car_bike         ,
                    service_cat      = service_cat      ,
                    job_name         = job_name         ,
                    doorstep         = doorstep         ,
                    default_components  = obj_default,
                    optional_components = obj_option,
                    total_price         = price_float_t_2,
                    total_price_comp    = price_float_c_2
                )
                serv.save()

def loadServiceLabour(fileName):
    with open(path+'/data revamp/'+fileName, 'rU') as csvfile:
        serviceData = csv.reader(csvfile, delimiter='\t', quotechar='|')
        i = 0
        for service in serviceData:
            i = i + 1
            print i
            city                = cleanstring(service[0])
            if city != "":
                vendor              = cleanstring(service[1])
                car_bike            = cleanstring(service[2])
                service_cat         = cleanstring(service[3])
                job_name            = cleanstring(service[4])
                job_sub_cat         = cleanstring(service[5])
                type                = cleanstring(service[6])
                total_price         = cleanstring(service[7])
                doorstep            = cleanstring(service[8])
                job_summary         = cleanstring(service[9]).split("$")
                time                = cleanstring(service[10])
                job_desc            = cleanstring(service[11])
                job_symptoms        = cleanstring(service[12]).split("$")
                job_features        = cleanstring(service[13]).split("$")
                price_active        = cleanstring(service[14])
                total_price_comp    = cleanstring(service[15])
                priority            = cleanstring(service[16])
                settlement_cat      = cleanstring(service[17])
            # print type
                findService = ServiceLabour.objects.filter(
                                city        =city,
                                vendor      = vendor,
                                car_bike    = car_bike,
                                service_cat = service_cat,
                                job_name    = job_name,
                                job_sub_cat = job_sub_cat,
                                type        = type,
                                doorstep    = doorstep
                )
                # print service_cat
                # print job_name
                if len(findService):
                    findService = findService[0]
                    print findService
                    findService.city = city
                    findService.vendor = vendor
                    findService.car_bike = car_bike
                    findService.service_cat = service_cat
                    findService.job_name = job_name
                    findService.job_sub_cat = job_sub_cat
                    findService.type = type
                    findService.total_price = round(float(total_price),0)
                    findService.doorstep = doorstep
                    findService.job_summary = job_summary
                    findService.time = time
                    findService.job_desc = job_desc
                    findService.job_symptoms = job_symptoms
                    findService.job_features = job_features
                    findService.total_price_comp = round(float(total_price_comp),0)
                    findService.price_active = price_active
                    findService.priority = priority
                    findService.save()
                    # print findService.job_name

                else:
                    serv = ServiceLabour(
                        city            = city              ,
                        vendor          = vendor            ,
                        car_bike        = car_bike          ,
                        service_cat     = service_cat       ,
                        job_name        = job_name          ,
                        job_sub_cat     = job_sub_cat      ,
                        type            = type              ,
                        total_price         = round(float(total_price),0)             ,
                        doorstep            = doorstep          ,
                        job_summary         = job_summary       ,
                        time                = time              ,
                        job_desc            = job_desc          ,
                        job_symptoms        = job_symptoms      ,
                        job_features        = job_features      ,
                        total_price_comp   = round(float(total_price_comp),0)        ,
                        price_active       = price_active            ,
                        priority     = priority,
                        settlement_cat = settlement_cat
                    )
                    print serv
                    serv.save()

def CreateJobList():
    AllVehicle = Vehicle.objects.all()
    for vehicle in AllVehicle:
        # print vehicle.full_veh_name
        # print vehicle.type
        # print vehicle.car_bike
        AllService = ServiceLabour.objects.filter(type = vehicle.type, car_bike = vehicle.car_bike)
        for service in AllService:
            # print service.job_name

            Parts = ServicePart.objects.filter(
                city=service.city,
                vendor=service.vendor,
                make=vehicle.make,
                model=vehicle.model,
                year=vehicle.year,
                fuel_type=vehicle.fuel_type,
                # full_veh_name=vehicle.full_veh_name,
                type=vehicle.type,
                car_bike=vehicle.car_bike,
                service_cat=service.service_cat,
                job_name=service.job_name,
                # doorstep=service.doorstep
            )

            # if vehicle.car_bike == "Bike":
            #     print vehicle.make
            #     print vehicle.model
            #     print vehicle.fuel_type
            #     print Parts
            #     print service.city
            #     print service.vendor
            #     print vehicle.year



            if len(Parts):
                Parts = Parts[0]
                # print Parts.total_price
                obj ={}
                obj['name'] = service.job_name
                obj['action'] = "Labour"
                obj['quantity'] = "1"
                obj['unit_price'] = str(service.total_price)
                obj['price'] = str(service.total_price)
                obj['category'] = "Labour"
                obj['price_comp'] = str(service.total_price_comp)
                obj['type'] = "Labour"
                obj['settlement_cat'] = service.settlement_cat
                # print obj
                # final_obj = []
                final_obj = Parts.default_components
                final_obj.append(obj)

                serv = Services(
                city 			= service.city,
                vendor              = service.vendor,
                car_bike 			= service.car_bike,
                service_cat			= service.service_cat,
                job_name 	        = service.job_name,
                job_sub_cat         = service.job_sub_cat,
                type                = service.type,
                total_price         = round((service.total_price + Parts.total_price),0),
                total_price_comp    = round((service.total_price_comp + Parts.total_price_comp),0),
                doorstep            = service.doorstep,
                year 				= vehicle.year,
                fuel_type 			= vehicle.fuel_type,
                full_veh_name 		= vehicle.full_veh_name,
                aspect_ratio 		= vehicle.aspect_ratio,
                job_summary         = service.job_summary,
                job_desc            = service.job_desc,
                job_symptoms        = service.job_symptoms,
                job_features        = service.job_features,
                time                = service.time,
                price_active        = service.price_active,
                priority            = service.priority,
                make 				= vehicle.make,
                model 				= vehicle.model,
                default_components  = final_obj,
                optional_components = Parts.optional_components,
                total_part          = Parts.total_price,
                total_labour        = (service.total_price),
                total_discount      = 0)
                serv.save()
            else:
                obj = {}
                obj['name'] = service.job_name
                obj['action'] = "Labour"
                obj['quantity'] = "1"
                obj['unit_price'] = service.total_price
                obj['price'] = service.total_price
                obj['category'] = "Labour"
                obj['price_comp'] = service.total_price_comp
                obj['type'] = "Labour"
                obj['settlement_cat'] = service.settlement_cat

                serv = Services(
                city 			    = service.city,
                vendor              = service.vendor,
                car_bike 			= service.car_bike,
                service_cat			= service.service_cat,
                job_name 	        = service.job_name,
                job_sub_cat         = service.job_sub_cat,
                type                = service.type,
                total_price         = round((service.total_price),0),
                total_price_comp    = round((service.total_price_comp),0),
                doorstep            = service.doorstep,
                year 				= vehicle.year,
                fuel_type 			= vehicle.fuel_type,
                full_veh_name 		= vehicle.full_veh_name,
                aspect_ratio 		= vehicle.aspect_ratio,
                job_summary         = service.job_summary,
                job_desc            = service.job_desc,
                job_symptoms        = service.job_symptoms,
                job_features        = service.job_features,
                time                = service.time,
                price_active        = service.price_active,
                priority            = service.priority,
                make 				= vehicle.make,
                model 				= vehicle.model,
                default_components  = [obj],
                optional_components = [],
                total_part          = 0,
                total_labour        = round((service.total_price),0),
                total_discount      = 0)
                serv.save()

def settlementCat():
    bookings = Bookings.objects.all()
    for booking in bookings:
        items = booking.service_items
        items_new = []
        print booking.booking_id
        for item in items:
            try:
                obj= {"name": item['name'],
                        "price": item['price'],
                        "type": item['type'],
                        "settlement_cat":item['settlement_cat']
                      }
                # print "Exist"
            except:
                try:
                    obj = {"name": item['name'],
                            "price": item['price'],
                            "type": item['type'],
                            "settlement_cat":item['type']}
                except:
                    obj = {"name": item['name'],
                           "price": item['price'],
                           "type": "Labour",
                           "settlement_cat": "Labour"}
                # print "Doesn't Exist"
            items_new.append(obj)
        booking.service_items = items_new
        booking.save()

def loadTaxes(fileName):
    with open(path+'/data revamp/'+fileName, 'rU') as csvfile:
        taxData = csv.reader(csvfile, delimiter=',', quotechar='|')
        for tax in taxData:
            state               = cleanstring(tax[0])
            vat_parts           = cleanstring(tax[1])
            vat_lubes           = cleanstring(tax[2])
            vat_consumable      = cleanstring(tax[3])
            service_tax         = cleanstring(tax[4])
            gst_parts           = cleanstring(tax[5])
            gst_lubes           = cleanstring(tax[6])
            gst_consumable      = cleanstring(tax[7])
            gst_service         = cleanstring(tax[8])

            findTax = Taxes.objects.filter(state=state)
            if len(findTax):
                findTax = findTax[0]
                findTax.state          = state
                findTax.vat_parts      = vat_parts
                findTax.vat_lubes      = vat_lubes
                findTax.vat_consumable = vat_consumable
                findTax.service_tax = service_tax

                findTax.gst_parts      = gst_parts
                findTax.gst_lubes      = gst_lubes
                findTax.gst_consumable = gst_consumable
                findTax.gst_service    = gst_service

                findTax.save()
            else:
                tax = Taxes(state=state,
                                     vat_parts=vat_parts,
                                     vat_lubes=vat_lubes,
                                     vat_consumable=vat_consumable,
                                     service_tax=service_tax,
                                     gst_parts=gst_parts,
                                     gst_lubes=gst_lubes,
                                     gst_consumable=gst_consumable,
                                     gst_service=gst_service
                )
                tax.save()




