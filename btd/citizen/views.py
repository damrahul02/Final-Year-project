from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Citizen, Applicant, Division, District, Subdistrict, Healthcare,Vaccine,VaccinationSchedule,Volunteer,Admin
from django.contrib.auth.hashers import make_password, check_password
import random
import datetime
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'citizen/index.html')

def citizen_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            citizen = Citizen.objects.get(username=username)
            if check_password(password, citizen.password):
                # Successful login
                request.session['citizen_id'] = citizen.id  # Store citizen ID in session
                request.session['username'] = citizen.username  # Store username in session
                return redirect('citizen:citizen_panel')  # Redirect to citizen panel after login
            else:
                messages.error(request, 'Invalid username or password')
        except Citizen.DoesNotExist:
            messages.error(request, 'Invalid username or password')
    return render(request, 'citizen/citizen_login.html')

def citizen_register(request):
    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if Citizen.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('citizen:citizen_register')

        if Citizen.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('citizen:citizen_register')

        # Hash the password before saving
        hashed_password = make_password(password)
        Citizen.objects.create(
            name=name,
            username=username,
            email=email,
            password=hashed_password
        )
        messages.success(request, 'Registration successful. You can now login.')
        return redirect('citizen:citizen_login')

    return render(request, 'citizen/citizen_register.html')

def citizen_panel(request):
    # Check if the user is logged in
    if 'citizen_id' not in request.session:
        return redirect('citizen:citizen_login')  # Redirect to login if not logged in

    citizen_id = request.session['citizen_id']
    
    citizen = Citizen.objects.get(id=citizen_id)  # Get the logged-in citizen's details

    return render(request, 'citizen/citizen_panel.html', {'citizen': citizen})
def citizen_profile(request):
    # Check if the user is logged in
    if 'citizen_id' not in request.session:
        return redirect('citizen:citizen_login')  # Redirect to login if not logged in

    citizen_id = request.session['citizen_id']
    citizen = Citizen.objects.get(id=citizen_id)  # Get the logged-in citizen's details

    return render(request, 'citizen/citizen_panel.html', {'citizen': citizen})
def citizen_pass(request):
    # Check if the user is logged in
    if 'citizen_id' not in request.session:
        return redirect('citizen:citizen_login')  # Redirect to login if not logged in

    citizen_id = request.session['citizen_id']
    citizen = Citizen.objects.get(id=citizen_id)  # Get the logged-in citizen's details

    return render(request, 'citizen/citizen_panel.html', {'citizen': citizen})
def citizen_update(request):
    # Check if the user is logged in
    if 'citizen_id' not in request.session:
        return redirect('citizen:citizen_login')  # Redirect to login if not logged in

    citizen_id = request.session['citizen_id']
    citizen = Citizen.objects.get(id=citizen_id)  # Get the logged-in citizen's details

    return render(request, 'citizen/citizen_panel.html', {'citizen': citizen})

def logout(request):
    # Clear the session
    request.session.flush()  # This will remove all session data
    messages.success(request, 'You have been logged out successfully.')
    return redirect('citizen:citizen_login')  # Redirect to login page after logout

def register_vaccine_part1(request):
    if request.method == 'POST':
        division_id = request.POST.get('division')
        district_id = request.POST.get('district')
        subdistrict_id = request.POST.get('subdistrict')
        healthcare_id = request.POST.get('healthcare')

        # Validate input
        if not all([division_id, district_id, subdistrict_id, healthcare_id]):
            messages.error(request, 'All fields are required.')
            return redirect('citizen:register_vaccine_part1')

        # Store data in session
        request.session['division_id'] = division_id
        request.session['district_id'] = district_id
        request.session['subdistrict_id'] = subdistrict_id
        request.session['healthcare_id'] = healthcare_id

        # Redirect to the baby registration page
        return redirect('citizen:register_baby')

    # Load divisions for the dropdown
    divisions = Division.objects.all()
    return render(request, 'citizen/register_vaccine_part1.html', {'divisions': divisions})

def register_baby(request):
    if request.method == 'POST':
        # Collect form data
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        full_name = request.POST['full_name']
        gender = request.POST['gender']
        religion = request.POST['religion']
        birth_country = request.POST['birth_country']
        birth_division_id = request.session.get('division_id')
        birth_district_id = request.session.get('district_id')
        birth_subdistrict_id = request.session.get('subdistrict_id')
        
        # Prepare birth date
        year = int(request.POST['selectYear'])
        month = request.POST['selectMonth']
        day = int(request.POST['selectDay'])

        # Convert month name to month number
        month_number = {
            "January": 1,
            "February": 2,
            "March": 3,
            "April": 4,
            "May": 5,
            "June": 6,
            "July": 7,
            "August": 8,
            "September": 9,
            "October": 10,
            "November": 11,
            "December": 12
        }.get(month)

        # Create a date object
        try:
            birth_date = datetime.date(year, month_number, day)
        except ValueError as e:
            messages.error(request, f'Invalid date: {e}')
            return redirect('citizen:register_baby')

        present_address = request.POST['present_address']
        permanent_address = request.POST['permanent_address']
        father_name = request.POST['fatherName']
        father_nid = request.POST['fatherNid']
        mother_name = request.POST['motherName']
        mother_nid = request.POST['motherNid']
        contact_number = request.POST['contact']
        relationship = request.POST['relationship']
        healthcare_id = request.session.get('healthcare_id')
        
        username = request.session.get('username')

        # Create an Applicant instance
        applicant = Applicant(
            application_id=generate_application_id(),  # You need to implement this function
            first_name=first_name,
            last_name=last_name,
            full_name=full_name,
            gender=gender,
            religion=religion,
            birth_country=birth_country,
            birth_division_id=birth_division_id,
            birth_district_id=birth_district_id,
            birth_subdistrict_id=birth_subdistrict_id,
            birth_date=birth_date,  
            present_address=present_address,
            permanent_address=permanent_address,
            father_name=father_name,
            father_nid=father_nid,
            mother_name=mother_name,
            mother_nid=mother_nid,
            contact_number=contact_number,
            relationship=relationship,
            division_id=birth_division_id,
            district_id=birth_district_id,
            subdistrict_id=birth_subdistrict_id,
            healthcare_id=healthcare_id,
            user_name=username  # Add the username to the applicant
        )
        applicant.save()

        # Fetch all vaccines
        vaccines = Vaccine.objects.all()

        if vaccines.exists():
            for vaccine in vaccines:
                time_intervals = vaccine.time_intervals  # Assuming this is a list of intervals in days
                for dose in range(1, vaccine.doses + 1):
                    # Calculate the scheduled date for the current dose
                    interval = time_intervals[dose - 1]  # Get the interval for the current dose (0-based index)
                    scheduled_date = birth_date + datetime.timedelta(days=int(interval))

                    # Create a VaccinationSchedule instance
                    vaccination_schedule = VaccinationSchedule(
                        application_id=applicant.application_id,
                        vaccine_id=vaccine.id,
                        dose_number=dose,
                        scheduled_date=scheduled_date,
                        healthcare_id=healthcare_id,
                        volunteer_id=None,
                        status="Pending"
                    )
                    vaccination_schedule.save()

        messages.success(request, 'Registration successful and vaccination scheduled!')
        return redirect('citizen:citizen_panel')

    # Load divisions for the dropdown
    divisions = Division.objects.all()
    
    # Pass session data to the template
    return render(request, 'citizen/register_baby.html', {
        'divisions': divisions,
        'division_id': request.session.get('division_id'),
        'district_id': request.session.get('district_id'),
        'subdistrict_id': request.session.get('subdistrict_id'),
        'healthcare_id': request.session.get('healthcare_id'),
    })

def generate_application_id():
    prefix = "BTD"
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    random_number = random.randint(1000, 9999)
    return f"{prefix}{timestamp}{random_number}"

def load_districts(request):
    division_id = request.GET.get('division_id')
    districts = District.objects.filter(division_id=division_id).values('id', 'name')
    return JsonResponse(list(districts), safe=False)

def load_subdistricts(request):
    district_id = request.GET.get('district_id')
    subdistricts = Subdistrict.objects.filter(district_id=district_id).values('id', 'name')
    return JsonResponse(list(subdistricts), safe=False)

def load_healthcare_centers(request):
    subdistrict_id = request.GET.get('subdistrict_id')
    healthcare_centers = Healthcare.objects.filter(subdistrict__id=subdistrict_id).values('id', 'name')
    return JsonResponse(list(healthcare_centers), safe=False)

def notification(request):
    # Check if the user is logged in
    if 'citizen_id' not in request.session:
        return redirect('citizen:citizen_login')  # Redirect to login if not logged in

    # Get the username from the session
    username = request.session.get('username')

    # Fetch all applicants associated with the logged-in user
    applicants = Applicant.objects.filter(user_name=username)

    if request.method == 'POST':
        selected_applicant_id = request.POST.get('applicant')
        if selected_applicant_id:
            # Fetch vaccination schedule for the selected applicant
            vaccination_schedules = VaccinationSchedule.objects.filter(application_id=selected_applicant_id)

            # Fetch vaccine details for the vaccination schedules
            vaccine_details = []
            for schedule in vaccination_schedules:
                vaccine = Vaccine.objects.get(id=schedule.vaccine_id)
                vaccine_details.append({
                    'vaccine_id': vaccine.id,
                    'vaccine_name': vaccine.vaccine_name,
                    'dose_number': schedule.dose_number,
                    'scheduled_date': schedule.scheduled_date,
                    'status': schedule.status,
                })

            return render(request, 'citizen/notification.html', {
                'applicants': applicants,
                'vaccine_details': vaccine_details,
                'selected_applicant_id': selected_applicant_id,
                
            })
        else:
            messages.error(request, 'Please select an applicant.')

    return render(request, 'citizen/notification.html', {
        'applicants': applicants,
    })

def generate_birth_certificate(request):
    # Check if the user is logged in
    if 'citizen_id' not in request.session:
        return redirect('citizen:citizen_login')  # Redirect to login if not logged in

    # Get the username from the session
    username = request.session.get('username')

    # Fetch all applicants associated with the logged-in user
    applicants = Applicant.objects.filter(user_name=username)

    if request.method == 'POST':
        selected_applicant_id = request.POST.get('applicant')
        if selected_applicant_id:
            # Fetch vaccination schedules for the selected applicant
            vaccination_schedules = VaccinationSchedule.objects.filter(application_id=selected_applicant_id)

            # Check if all vaccinations are done
            all_done = all(schedule.status == "Done" for schedule in vaccination_schedules)

            if all_done:
                # Generate birth certificate data
                applicant = Applicant.objects.get(application_id=selected_applicant_id)
                return render(request, 'citizen/birth_certificate.html', {
                    'applicant': applicant,
                    'vaccination_schedules': vaccination_schedules,
                })
            else:
                messages.error(request, 'Please complete all vaccinations before generating the birth certificate.')
                return redirect('citizen:generate_birth_certificate')

    return render(request, 'citizen/generate_birth_certificate.html', {
        'applicants': applicants,
    })

def volunteer_login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        try:
            volunteer = Volunteer.objects.get(email=email)
            # if check_password(password, volunteer.password):
            if (password==volunteer.password):
                request.session['volunteer_id'] = volunteer.id
                request.session['volunteer_name'] = volunteer.name
                request.session['volunteer_email'] = volunteer.email
                request.session['volunteer_healthcare'] = volunteer.healthcare
                request.session['volunteer_subdistrict_id'] = volunteer.subdistrict_id
                request.session['healthcare_id'] = volunteer.healthcare_id
                messages.success(request, 'Login successful!')
                print("xd")
                return redirect('citizen:volunteer_panel')
            else:
                messages.error(request, "Invalid email or password.")
                print("fuck")
        except Volunteer.DoesNotExist:
            messages.error(request, "Invalid email or password.")
    return render(request, 'citizen/volenteer.html')


def volunteer_panel(request):

    if 'volunteer_id' not in request.session:
        return redirect('citizen:volunteer_login')  

    citizen_id = request.session['volunteer_id']
    
    citizen = Volunteer.objects.get(id=citizen_id) 

    return render(request, 'citizen/volenteer_panel.html', {'citizen': citizen})

def admin_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']

        try:
            # Check if an admin with this email and role exists
            admin = Admin.objects.get(email=email, role=role)
            
            # Verify the password
            # if check_password(password, admin.password):
            if (password==admin.password):
                # Store admin session details
                request.session['admin_id'] = admin.id
                request.session['admin_name'] = admin.name
                request.session['admin_role'] = admin.role
                
                # Redirect based on role
                if role == 'Division':
                    return redirect('/dashboard/divisional')
                elif role == 'District':
                  return redirect('citizen:district_dashboard') 
                elif role == 'Sub district':
                    return redirect('/dashboard/subdistrict')
            else:
                messages.error(request, 'Invalid password. Please try again.')
        except Admin.DoesNotExist:
            messages.error(request, 'Invalid credentials or role. Please try again.')

    return render(request, 'citizen/admin_login.html')
@login_required
def district_dashboard(request):
    if request.user.is_authenticated and request.session.get('admin_role') == 'District':
        district_id = request.user.district_id  # Ensure this attribute exists

        # Fetch sub-district admins for this district
        subdistrict_admins = Admin.objects.filter(role="Sub district", district_id=district_id)

        if request.method == "POST":
            # Handle form submission to add a new sub-district admin
            name = request.POST['name']
            email = request.POST['email']
            password = request.POST['password']
            subdistrict_id = request.POST['subdistrict_id']

            try:
                new_admin = Admin.objects.create(
                    name=name,
                    email=email,
                    password=make_password(password),  # Hash the password
                    role="Sub district",
                    district_id=district_id,
                    subdistrict_id=subdistrict_id
                )
                messages.success(request, "Sub-district admin added successfully.")
                return redirect('district_dashboard')
            except Exception as e:
                messages.error(request, f"Error adding sub-district admin: {e}")

        subdistricts = Subdistrict.objects.filter(district_id=district_id)

        return render(request, 'district-admin.html', {
            'subdistrict_admins': subdistrict_admins,
            'subdistricts': subdistricts
        })
    else:
        return redirect('citizen:admin_login')  # Redirect to the correct login URL