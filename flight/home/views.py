from django.shortcuts import render
from django.contrib import messages
import pandas as pd
import numpy as np
import pickle

def main(request):
    if request.method=="POST":
        departure_date = request.POST['Departure_Date']
        arrival_date = request.POST['Arrival_Date']
        source = request.POST['Source']
        destination = request.POST['Destination']
        airline = request.POST['Airline']
        stopage = request.POST['Stopage']

        total_stops = int(stopage)

        journey_day = pd.to_datetime(departure_date, format="%Y-%m-%dT%H:%M").day
        journey_mth = pd.to_datetime(departure_date, format="%Y-%m-%dT%H:%M").month
        dep_hr = pd.to_datetime(departure_date, format="%Y-%m-%dT%H:%M").hour
        dep_min = pd.to_datetime(departure_date, format="%Y-%m-%dT%H:%M").minute

        arr_day = pd.to_datetime(arrival_date, format="%Y-%m-%dT%H:%M").day
        arr_hr = pd.to_datetime(arrival_date, format="%Y-%m-%dT%H:%M").hour
        arr_min = pd.to_datetime(arrival_date, format="%Y-%m-%dT%H:%M").minute


        if journey_day < arr_day:
            duration_hr = abs((arr_hr+24) - dep_hr)
            duration_min = abs(arr_min - dep_min)
        else:
            duration_hr = abs(arr_hr - dep_hr)
            duration_min = abs(arr_min - dep_min)


        air = str(airline)
        src= str(source)
        dest = str(destination)

        features = [total_stops,journey_day,journey_mth,dep_hr,dep_min,arr_hr,arr_min,duration_hr,duration_min,'Airline_Air India','Airline_GoAir','Airline_IndiGo','Airline_Jet Airways','Airline_Jet Airways Business','Airline_Multiple carriers','Airline_Multiple carriers Premium economy','Airline_SpiceJet','Airline_Trujet','Airline_Vistara','Airline_Vistara Premium economy','Source_Chennai','Source_Delhi','Source_Kolkata','Source_Mumbai','Destination_Cochin','Destination_Delhi','Destination_Hyderabad','Destination_Kolkata','Destination_New Delhi']

        for i in range(len(features)):

            if 'Airline' in str(features[i]):
                if air == str(features[i]).split('_')[1]:
                    features[i] = 1
                else:
                    features[i] = 0 

            if 'Source' in str(features[i]):
                if src in str(features[i]):
                    features[i] = 1
                else:
                    features[i] = 0 

            if 'Destination' in str(features[i]):
                if dest in str(features[i]):
                    features[i] = 1
                else:
                    features[i] = 0

        print(features)                         

        data = np.array([features])  
        file = open(r'F:\Desktop\Aquib extras\Machine Learning\Flight-Price-Prediction\flight.pkl','rb')
        model = pickle.load(file)
        price = model.predict(data)

        messages.success(request,round(price[0],2))
                                     


    return render(request,'base.html')