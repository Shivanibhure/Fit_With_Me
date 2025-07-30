from django.shortcuts import render, redirect
from django.urls import reverse

from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache

import openai
from django.shortcuts import render

from django.conf import settings  
from .services import Dataoperations


def index(request):
    return render(request,'index.html')

def login(request):
    return render(request,'login.html')

@csrf_protect
def userlogin(request):
    if request.method == "POST":
        unm = request.POST.get("username")
        ups = request.POST.get("password")
        if unm == "shivani" and ups == "bhure":
            request.session["is_logged_in"]=True
            request.session["username"] = unm
            return redirect('dashboard')
        else:
            return render(request,"loginfailed.html",{"error":"Invalid credentials"})

@never_cache         
def dashboard(request):
    if not request.session.get("is_logged_in"):
        return redirect('')
    
    nm=request.session.get("username")
    return render(request,"dashboard.html",{"user":nm})


def add_profile(request):
    return render(request,'add_profile.html')



def profile_added(request):
    if request.method == "POST":
        name = request.POST.get("person_name")
        age = int(request.POST.get("age"))
        gender = request.POST.get("gender")
        height_cm = float(request.POST.get("height_cm"))
        weight = int(request.POST.get("weight_kg"))
        bmi = float(request.POST.get("bmi"))
        food = request.POST.get("food_type")
        step = int(request.POST.get("steps_per_day"))
        fs = Dataoperations()
        result = fs.add_profile(name, age, gender, height_cm, weight, bmi, food, step)
        if result:
            return render(request, 'p_added_successfully.html', {"msg": "Profile added successfully"})
        else:
            return render(request, 'profile_not_added.html', {"msg": "Profile not added"})
    
                

        
"""
def modify_profile(request):

    # Modify profile logic
    return render(request, 'update_profile.html')

def show_profile_name(request):
    fs = Dataoperations()
    list_of_username = fs.list_of_users()
    profiles = []
    for row in list_of_username:
        profiles.append({
            'profile_id': row[0],
            'person_name': row[1]
        })

    return render(request, 'list_profile_name.html', {'profiles': profiles})

"""        


def update_profile_view(request, person_name):
    if request.method == 'POST':
        age = int(request.POST.get('age'))
        gender = request.POST.get('gender')
        height = float(request.POST.get('height_cm'))
        weight = int(request.POST.get('weight_kg'))
        bmi = float(request.POST.get('bmi'))
        food = request.POST.get('food_type')
        steps = int(request.POST.get('steps_per_day'))

        dao = Dataoperations()
        updated = dao.update_profile(person_name, age, gender, height, weight, bmi, food, steps)

        if updated:
            return render(request, 'profile_update_done.html', {'msg': 'Profile updated successfully!'})
        else:
            return render(request, 'profile_not_updated.html', {'msg': 'Failed to update profile.'})


def delete_profile(request):
    # Delete profile logic
    message = None
    try:
        if request.method == 'POST' and 'profile_id' in request.POST:
            profile_id = int( request.POST.get('profile_id'))
            data = Dataoperations()
            deleted = data.delete_profile(profile_id)

            if deleted:
                return render(request, 'delete_profile.html', {'message': 'Profile deleted successfully!'})
            else:
                return render(request, 'delete_profile.html', {'message': 'Profile not found.'})
    except ValueError:
            # Handle the case where profile_id is not an integer
        return render(request, 'delete_profile.html', {'message': 'Invalid profile ID. Please enter a valid number.'})
    return render(request, 'delete_profile.html')

def generate_report(request):
    # Report generation logic
    data = Dataoperations()
    profile = data.report()
    return render(request, 'report.html',{'profile': profile})
"""
def generate_ai_recommendation(request,profile_id):
    
    if request.method == 'POST' and 'profile_id' in request.POST:
        try:
            name = int(request.POST.get('profile_id'))
            dao = Dataoperations()
            profile_data = dao.get_profile_by_id(name)

            if profile_data:
                profile = {
                    'person_name': profile_data[0],
                    'age': profile_data[1],
                    'gender': profile_data[2],
                    'height_cm': profile_data[3],
                    'weight_kg': profile_data[4],
                    'bmi': profile_data[5],
                    'food_type': profile_data[6],
                    'steps_per_day': profile_data[7],
                }
    # AI recommendation logic
    return render(request, 'recommendation.html')
"""


# Set your OpenAI API key here (or better, store in environment or settings)
 # Replace with your key or use: settings.OPENAI_API_KEY
#openai.api_key = settings.OPENAI_API_KEY 

import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_ai_recommendation(request, profile_id=None):
    if request.method == 'POST' and 'profile_id' in request.POST:
        try:
            profile_id = int(request.POST.get('profile_id'))
            dao = Dataoperations()
            profile_data = dao.get_profile_by_id(profile_id)

            if profile_data:
                profile = {
                    'person_name': profile_data[0],
                    'age': profile_data[1],
                    'gender': profile_data[2],
                    'height_cm': profile_data[3],
                    'weight_kg': profile_data[4],
                    'bmi': profile_data[5],
                    'food_type': profile_data[6],
                    'steps_per_day': profile_data[7],
                }

                # Create the prompt
                prompt = f"""
                    Create a personalized daily diet recommendation for the following user, formatted in HTML with <strong> tags for headings:
                    - Name: {profile['person_name']}
                    - Age: {profile['age']}
                    - Gender: {profile['gender']}
                    - Height: {profile['height_cm']} cm
                    - Weight: {profile['weight_kg']} kg
                    - BMI: {profile['bmi']}
                    - Food Preference: {profile['food_type']}
                    - Steps per day: {profile['steps_per_day']}

                    Format the response with:
                    - <strong>Meal headers</strong> (like Breakfast, Lunch, etc.)
                    - Bullet points for food items
                    - A <strong>Total Daily Calories</strong> and <strong>Macronutrient Split</strong> section
                    """

                # Call OpenAI
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a certified nutritionist."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=600
                )

                recommendation = response['choices'][0]['message']['content']

                return render(request, 'recommendation.html', {
                    'profile': profile,
                    'recommendation': recommendation
                })

            else:
                return render(request, 'recommendation.html', {
                    'error': 'No profile found for the given ID.'
                })

        except ValueError:
            return render(request, 'recommendation.html', {
                'error': 'Invalid Profile ID.'
            })

    return render(request, 'recommendation.html')


def search_update(request):
    profile = None

    if request.method == 'POST' and 'profile_id' in request.POST:
        try:
            name = int(request.POST.get('profile_id'))
            dao = Dataoperations()
            profile_data = dao.get_profile_by_id(name)

            if profile_data:
                profile = {
                    'person_name': profile_data[0],
                    'age': profile_data[1],
                    'gender': profile_data[2],
                    'height_cm': profile_data[3],
                    'weight_kg': profile_data[4],
                    'bmi': profile_data[5],
                    'food_type': profile_data[6],
                    'steps_per_day': profile_data[7],
                }
        except ValueError:
            # Handle the case where profile_id is not an integer
            return render(request, 'update_profile.html', {'error_message': 'Invalid profile ID. Please enter a valid number.'})


    return render(request, 'update_profile.html', {'profile': profile})

@never_cache
def logout(request):
    if request.session.get("is_logged_in"):
        request.session["is_logged_in"] = False
        
        return redirect(reverse('index'))
        

