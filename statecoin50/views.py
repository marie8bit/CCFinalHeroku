from django.shortcuts import render, get_object_or_404, render_to_response
from .models import Coin
from .forms import CoinCollectorForm, CoinDetailForm, UserRegistrationForm
from django.http import HttpResponse
from django.template import Context, loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.utils import timezone
import json
import folium


# Create your views here.
@login_required
def coin_collector(request, user_pk):
    user = User.objects.get(pk=user_pk)
    coins = Coin.objects.filter(owner = user).order_by('state')

    if not (coins):
        states_abbr = json.load(open('statecoin50/fixtures/us_states_abbr.json.txt'))
        f = open('statecoin50/fixtures/50sqReport.txt', 'rb').read()
        text = f.decode('utf-16')
        textn = text.replace('\n', '')
        state_dets = textn.split('\r')
        caseDetsLower = []
        for line in state_dets:
            lline = line.lower()
            caseDetsLower.append(lline)
        for key in states_abbr:
            state = key
            abr= states_abbr[key]
            owned = False
            url= 'resources/stateImage/'+abr+'.jpg'
            caseState = state.lower()
            dex = caseDetsLower.index(caseState)
            dates = state_dets[dex+1]
            details = state_dets[dex+2]
            coin = Coin(owner = user, state = state, stAbbr = abr, owned= owned, stImg=url, dates = dates, details = details)
            coin.save()
            map_us = folium.Map(location=[40, -102], zoom_start=3)
            #map_us.geo_json(geo_path = statesOwned, data = statesOwned, columns=['State','Owned'], fill_color = 'YlGn', fill_opacity=0.7, line_opacity =0.2)
            map_us.save('statecoin50/templates/statecoin50/map_coins.html')
            coins = Coin.objects.filter(owner = user).order_by('state')
            ownedCount= Coin.objects.filter(owner=user).filter(owned=True).count()
            if (ownedCount==0):
                message= 'You have not collected any coins yet'
            elif(ownedCount==1):
                message='You have collected '+str(ownedCount)+'coin'
            else:
                message='You have collected '+str(ownedCount)+'coins'
        return render(request, 'statecoin50/coin_collector.html', {'coins':coins, 'message':message})
    else:
        statesOwned = Coin.objects.filter(owner = user).order_by('stAbbr')


        all_state_map={}
        for coin in statesOwned:
            if coin.owned:
                number = 10
            else:
                number = 1
            all_state_map[coin.stAbbr]=number

        map_us = folium.Map(location=[50, -118], zoom_start=3)
        us_states_file='statecoin50/fixtures/us_states.json'

        map_us.choropleth(geo_path = us_states_file,
                        data = all_state_map,
                        columns=['state','number'],
                        key_on='id',
                        fill_color = 'YlGn', fill_opacity=0.7, line_opacity =0.2,
                        threshold_scale = [1,3,5,7,10],
                        legend_name = "Coins Collected: Yellow= Not Collected - Green = Collected")
        map_us.save('statecoin50/templates/statecoin50/map_coins.html')
        ownedCount= Coin.objects.filter(owner=user).filter(owned=True).count()
        if (ownedCount==0):
            message= 'You have not collected any coins yet'
        elif(ownedCount==1):
            message='You have collected '+str(ownedCount)+' coin'
        else:
            message='You have collected '+str(ownedCount)+' coins'
        return render(request, 'statecoin50/coin_collector.html', {'coins':coins, 'message':message})


@login_required
def collection_wishlist(request, user_pk):
    user = User.objects.get(pk=user_pk)
    coins = Coin.objects.filter(owner = user).order_by('state')
    if not (coins):
        states_abbr = json.load(open('statecoin50/fixtures/us_states_abbr.json.txt'))
        f = open('statecoin50/fixtures/50sqReport.txt', 'rb').read()
        text = f.decode('utf-16')
        textn = text.replace('\n', '')
        state_dets = textn.split('\r')
        caseDetsLower = []
        for line in state_dets:
            lline = line.lower()
            caseDetsLower.append(lline)
        for key in states_abbr:
            state = key
            abr= states_abbr[key]
            owned = False
            url= 'resources/stateImage/'+abr+'.jpg'
            caseState = state.lower()
            dex = caseDetsLower.index(caseState)
            dates = state_dets[dex+1]
            details = state_dets[dex+2]
            coin = Coin(owner = user, state = state, stAbbr = abr, owned= owned, stImg=url, dates = dates, details = details)
            coin.save()
            map_us = folium.Map(location=[40, -102], zoom_start=3)
            #map_us.geo_json(geo_path = statesOwned, data = statesOwned, columns=['State','Owned'], fill_color = 'YlGn', fill_opacity=0.7, line_opacity =0.2)
            map_us.save('statecoin50/templates/statecoin50/map_coins.html')
            coins = Coin.objects.filter(owner = user).order_by('state')
        return render(request, 'statecoin50/coin_collector.html', {'coins':coins})
    else:
        statesOwned = Coin.objects.filter(owner = user).order_by('stAbbr')


        all_state_map={}
        for coin in statesOwned:
            if coin.owned:
                number = 1
            else:
                number = 10
            all_state_map[coin.stAbbr]=number

        map_us = folium.Map(location=[50, -118], zoom_start=3)
        us_states_file='statecoin50/fixtures/us_states.json'

        map_us.choropleth(geo_path = us_states_file,
                        data = all_state_map,
                        columns=['state','number'],
                        key_on='id',
                        fill_color = 'PuBuGn', fill_opacity=0.7, line_opacity =0.2,
                        threshold_scale = [1,3,5,7,10],
                        legend_name = "Dark Blue = Coins not collected")
        map_us.save('statecoin50/templates/statecoin50/map_wishlist.html')
        return render(request, 'statecoin50/collection_wishlist.html', {'coins':coins})

@login_required
def coindetail(request, coin_pk):
    coin = get_object_or_404(Coin, pk=coin_pk)
    form = CoinDetailForm(request.POST)
    if request.method == "POST":

        if form.is_valid():
            coin2=form.save(commit = False)
            coin.owned=True
            coin.dateOwned=(timezone.now())
            coin.save()

            return render(request, 'statecoin50/coindetail.html', {'coin':coin}, {'form':form})
        else:
            print('form is not valid')
    else:
        form = CoinDetailForm(instance = coin)
        statesOwned = Coin.objects.filter(owner = coin.owner).order_by('stAbbr')
        all_state_map={}
        for item in statesOwned:
            if (coin.stAbbr == item.stAbbr):
                number = 10
            else:
                number = 1
            all_state_map[item.stAbbr]=number

        #source reference https://gist.githubusercontent.com/meiqimichelle/7727723/raw/0109432d22f28fd1a669a3fd113e41c4193dbb5d/USstates_avg_latLong
        location = json.load(open('statecoin50/fixtures/USstates_avg_latLong.json'))

        for d in location:
            state = d['state']
            lat =d['latitude']
            lon =d['longitude']
            # print(state)
            # print(lat)
            # print(lon)
            # print(coin.state)
            if (state == coin.state):
                if (state =='Alaska'):
                    map_us = folium.Map(location=[lat, lon], zoom_start=4)
                elif(state=='Colorado' or state =='California' or state=='Idaho'
                    or state=='Florida' or state=='Kansas' or state=='Kentucky'
                    or state=='Michigan' or state=='Minnesota' or state=='Montana'
                    or state=='Nebraska' or state=='Nevada' or state=='New Mexico'
                    or state=='New York' or state=='North Carolina' or state=='North Dakota'
                    or state=='Oklahoma' or state=='Oregon' or state=='South Dakota'
                    or state=='Tennessee'  or state =='Virginia'
                    or state =='Washington' or state =='Wyoming'):
                    map_us = folium.Map(location=[lat, lon], zoom_start=6)
                elif(state =='Texas'):
                    map_us = folium.Map(location=[lat, lon-2.5], zoom_start=6)
                else:
                    map_us = folium.Map(location=[lat, lon], zoom_start=7)
                break
            else:
                map_us = folium.Map(location=[50, -118], zoom_start=3)
        us_states_file='statecoin50/fixtures/us_states.json'

        map_us.choropleth(geo_path = us_states_file,
                        data = all_state_map,
                        columns=['state','number'],
                        key_on='id',
                        fill_color = 'YlGn', fill_opacity=0.7, line_opacity =0.2,
                        threshold_scale = [1,3,5,7,10],
                        legend_name = coin.state+" State Map")
        map_us.save('statecoin50/templates/statecoin50/state_map.html')
        return render(request, 'statecoin50/coindetail.html', {'coin':coin}, {'form':form})

#source reference http://stackoverflow.com/questions/14400035/how-to-return-a-static-html-file-as-a-response-in-django
#http://stackoverflow.com/questions/17168256/template-does-not-exist


def homepage(request):
    userCount = User.objects.count()
    coinCount = Coin.objects.filter(owned=True).count()

    #print(coinCount)
    return render(request, 'statecoin50/home.html', {'coinCount':coinCount, 'userCount':userCount})


def register(request):

    if request.method == 'POST':

        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])

            login(request, user)
            if request.user.is_authenticated():  # If userprofile object has a user object property

                coins = Coin.objects.filter(owner = request.user).order_by('state')
                return render(request, 'statecoin50/coin_collector.html', {'coins':coins})
            else:
                message = ValidationError.message
                return render(request, 'registration/register.html', { 'form' : form , 'message' : message } )
        else :
            message = 'Please check the data you entered'
            return render(request, 'registration/register.html', { 'form' : form , 'message' : message } )


    else:
        form = UserRegistrationForm()
        return render(request, 'registration/register.html', { 'form' : form } )
