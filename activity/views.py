# Create your views here.
# from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from authomatic import Authomatic
from authomatic.adapters import DjangoAdapter

from django.core.context_processors import csrf
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from activity.models import CGUser

from social.apps.django_app.utils import psa

from django.views.decorators.csrf import csrf_exempt

from config import CONFIG

authomatic = Authomatic(CONFIG, 'facf8eedf58febc4a32b07129785ff70')

from api.models import Car

def social_login(request, provider_name):
    response = HttpResponse()
    print request
    if provider_name == 'fb':
        result = authomatic.login(DjangoAdapter(request, response), provider_name)
        if result:
            response.write('<a href="..">Home</a>')
            if result.error:
                response.write('<h2>Damn that error: {0}</h2>'.format(result.error.message))
            elif result.user:
                if not (result.user.name and result.user.id):
                    result.user.update()
                    response.write(u'<h1>Hi {0}</h1>'.format(result.user.name))
                    response.write(u'<h2>Your id is: {0}</h2>'.format(result.user.id))
                    response.write(u'<h2>Your email is: {0}</h2>'.format(result.user.email))
                    if result.user.email:
                        if user_exists(result.user.email):
                            pw = User.objects.filter(username=result.user.email)
                            pw = pw[0].password
                            user = authenticate(username=result.user.email, password=pw)
                            if user is not None:
                                login(request, user)
                                response.write('user logged in')
                                # return redirect('/')
                            else:
                                response.write('user not logged in')
                                # return redirect('/')

                    if result.user.credentials:
                        if result.provider.name == 'fb':
                            response.write('Your are logged in with Facebook.<br />')
                            url = 'https://graph.facebook.com/{0}?fields=id,name,email'
                            # url = 'https://graph.facebook.com/v2.0/?fields=id,name,email'
                            url = url.format(result.user.id)
                            access_response = result.provider.access(url)
                            print access_response.status
                            if access_response.status == 200:
                            # Parse response.
                                print access_response.data
    #                            statuses = access_response.data.get('feed').get('data')
                                error = access_response.data.get('error')
                                response.write(access_response.data)
                                if error:
                                    response.write(u'Damn that error: {0}!'.format(error))
                                # elif statuses:
                                #     response.write('Your 5 most recent statuses:<br />')
     #                               for message in statuses:

      #                                  text = message.get('message')
       #                                 date = message.get('created_time')

    #                                    response.write(u'<h3>{0}</h3>'.format(text))
     #                                   response.write(u'Posted on: {0}'.format(date))
                                else:
                                    response.write('barely functional')

                            else:
                                response.write('Damn that unknown error!<br />')
                                # response.write(u'Status: {0}'.format(response.status))

                        if result.provider.name == 'tw':
                            response.write('Your are logged in with Twitter.<br />')

                            # We will get the user's 5 most recent tweets.
                            url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'

                            # You can pass a dictionary of querystring parameters.
                            access_response = result.provider.access(url, {'count': 5})

                            # Parse response.
                            if access_response.status == 200:
                                if type(access_response.data) is list:
                                    # Twitter returns the tweets as a JSON list.
                                    response.write('Your 5 most recent tweets:')
                                    for tweet in access_response.data:
                                        text = tweet.get('text')
                                        date = tweet.get('created_at')

                                        response.write(u'<h3>{0}</h3>'.format(text))
                                        response.write(u'Tweeted on: {0}'.format(date))

                                elif response.data.get('errors'):
                                    response.write(u'Damn that error: {0}!'.\
                                                        format(response.data.get('errors')))
                            else:
                                response.write('Damn that unknown error!<br />')
                                response.write(u'Status: {0}'.format(response.status))
    elif provider_name == 'cg':
        return auth_and_login(request)


    return response

def loginview(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('login.html', c)

@csrf_exempt
def auth_and_login(request, onsuccess='/', onfail='/loginPage/'):
    user = authenticate(username=request.POST['email'], password=request.POST['password'])
    if user is not None:
        login(request, user)
        return redirect(onsuccess)
    else:
        return redirect(onfail)

def logout_to_home(request):
    auth_logout(request)
    return HttpResponseRedirect('http://www.clickgarage.in/')

def create_user(username, email, password):
    user = CGUser(username=username, email=email)
    user.set_password(password)
    user.save()
    return user

def user_exists(email):
    user_count = CGUser.objects.filter(email=email).count()
    if user_count == 0:
        return False
    return True

@csrf_exempt
def sign_up_in(request):
    post = request.POST
    if not user_exists(post['email']):
        user = create_user(username=post['email'], email=post['email'], password=post['password'])
    	return auth_and_login(request)
    else:
    	return redirect("/loginPage/")

@login_required(login_url='/login/')
def secured(request):
    return render_to_response("secure.html")

@psa('social:complete')
def register_by_access_token(request, backend):
    # This view expects an access_token GET parameter, if it's needed,
    # request.backend and request.strategy will be loaded with the current
    # backend and strategy.
    token = request.GET.get('access_token')
    if token:
        user = request.backend.do_auth(request.GET.get('access_token'))
        if user:
            login(request, user)
            return True
        else:
            return False
    else:
        return False

def updateCart(user, cookie_data, action, car_id):
    item = cookie_data
    iuser = user
    cartItems = iuser.uc_cart
    if len(item):
        items = item.split(",")
        for i in items:
            timestamp = i.split('*')[0]
            # cartObj['dealer_id'] = i.split('*')[3]
            # present = False
            # for io in cartItems:
            #     if 'timestamp' in io and io['timestamp'] == timestamp:
            #         present = True
            #         if action == 'delete':
            #             cartItems.remove(io)
            #
            # if not present:
            #     if action == 'add':
            #         cartItems.append(cartObj)

            if timestamp in cartItems:
                if action == 'delete':
                    del cartItems[timestamp]
            else:
                if action == 'add':
                    cartObj = {}
                    if car_id:
                        car = Car.objects.filter(id=car_id)
                        if len(car):
                            car = car[0]
                            cartObj['car'] = {
                                'name':car.name,
                                'model':car.model,
                                'make':car.make,
                                'year':car.year,
                                'size':car.size,
                                
                            }

                    # cartObj['timestamp'] = timestamp
                    cartObj['service'] = i.split('*')[1]
                    cartObj['dealer'] = i.split('*')[2]
                    cartObj['service_id'] = i.split('*')[3]
                    cartItems[timestamp] = cartObj

            iuser.uc_cart = cartItems
            iuser.save()

