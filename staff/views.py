from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import SignupForm
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Voter
from django.http import JsonResponse
from django.db.utils import IntegrityError
from .models import Candidate

from django.contrib.auth.decorators import login_required
from .models import AdminProfile


################HOME PAGE##############
def home(request):
    return render(request, 'home.html')

def dashboard(request):
    # Get the logged-in user's profile, or use a default profile if not found
    profile = get_object_or_404(AdminProfile, user=request.user)

    context = {
        'profile': profile  # Pass the profile object to the template
    }
    return render(request, 'admin_panel.html', context)


def logout_view(request):
    logout(request)  # Logs out the user
    return redirect('home')  # Redirect to the home page


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Create the new user
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            user_id = user.id  # Get the user's ID

            # Log the user in automatically after registration
            login(request, user)
            return redirect('dashboard')  # Redirect to home after successful registration
        else:
            # Pass the form errors to the template
            return render(request, 'signing.html', {'form': form, 'signup_errors': form.errors})

    else:
        form = SignupForm()

    return render(request, 'signing.html', {'form': form})

def signin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Ensure email and password are provided
        if not email or not password:
            messages.error(request, "Both email and password are required.", extra_tags="login_error")
            return redirect('signin')

        # Get user by email
        user = User.objects.filter(email=email).first()

        if user:
            authenticated_user = authenticate(request, username=user.username, password=password)
            if authenticated_user:
                auth_login(request, authenticated_user)
                return redirect(reverse('dashboard'))  # Redirect to dashboard
            else:
                messages.error(request, "Invalid email or password.", extra_tags="login_error")
        else:
            messages.error(request, "Invalid email or password.", extra_tags="login_error")

    return render(request, 'signin.html')  # Ensure the correct template name


    
from django.shortcuts import render

def panel(request):
    return render(request, 'dashboard.html')


def add_voter(request):
    profile = get_object_or_404(AdminProfile, user=request.user)

    if request.method == 'POST':
        name = request.POST['voter_name']
        email = request.POST['voter_email']
        reg_number = request.POST['reg_number']
        department = request.POST['department']

        # Check if the voter already exists
        if Voter.objects.filter(reg_number=reg_number).exists():
            return render(request, 'errors.html', {'error_message': "Voter is already registered!"})

        # Generate department code prefix
        department_codes = {
            "Accounting & Finance": "AF",
            "Business Administration & Management": "BA",
            "Economics & Statistics": "ES",
            "Software Development & Information": "SD",
            "Applied Computing & Network": "AC",
            "Education & Physical Studies": "EP",
            "Performing Arts, Film, Media & Economic Studies": "PA"
        }

        prefix = department_codes.get(department, "XX")  # Default to XX if department not found
        last_voter = Voter.objects.filter(department=department).order_by('-id').first()

        if last_voter and last_voter.voter_code.startswith(prefix):
            last_number = int(last_voter.voter_code[len(prefix):])  # Extract numeric part
            new_number = last_number + 1
        else:
            new_number = 1

        voter_code = f"{prefix}{new_number}"  # Generate new voter code

        # Save voter to the database
        try:
            new_voter = Voter(name=name, email=email, reg_number=reg_number, department=department, voter_code=voter_code)
            new_voter.save()
            messages.success(request, "Voter added successfully!")
        except IntegrityError:
            return render(request, 'errors.html', {'error_message': "Error: A voter with this email or registration number already exists."})

        return redirect('add_voter')  # Redirect to dashboard after successful registration

    return render(request, 'add_voter.html' , {'profile': profile})




def add_candidate(request):
    profile = get_object_or_404(AdminProfile, user=request.user)

    if request.method == 'POST':
        name = request.POST.get('candidateName')
        email = request.POST.get('candidateEmail')
        admission_number = request.POST.get('admissionNumber')
        course = request.POST.get('course')
        department = request.POST.get('department')
        profile_picture = request.FILES.get('profilePicture')

        # Check if candidate with the same email or admission number exists
        if Candidate.objects.filter(email=email).exists() or Candidate.objects.filter(admission_number=admission_number).exists():
            return render(request, 'errors.html', {'error_message': 'Candidate already exists!'})

        try:
            new_candidate = Candidate(
                name=name,
                email=email,
                admission_number=admission_number,
                course=course,
                department=department,
                profile_picture=profile_picture
            )
            new_candidate.save()
            messages.success(request, "Candidate added successfully!")
            return redirect('add_candidate')  # Redirect to dashboard after successful addition
        except IntegrityError:
            messages.error(request, "An error occurred while adding the candidate.")
            return render(request, 'add_candidate.html')

    return render(request, 'add_candidate.html', {'profile': profile})




def tables(request):
    # Fetch all voters and candidates
    voters = Voter.objects.all()
    candidates = Candidate.objects.all()

    # Get the logged-in user's profile
    profile = get_object_or_404(AdminProfile, user=request.user)

    return render(request, 'tables.html', {
        'voters': voters,
        'candidates': candidates,
        'profile': profile  # Pass profile to template
    })



def reports(request):
    # Get all unique departments
    departments = Voter.objects.values_list('department', flat=True).distinct()

    # Calculate total voters and candidates per department
    department_data = []
    for department in departments:
        voter_count = Voter.objects.filter(department=department).count()
        candidate_count = Candidate.objects.filter(department=department).count()
        department_data.append({
            'department': department,
            'voters': voter_count,
            'candidates': candidate_count
        })

    # Prepare data for Pie Chart (Total voters per department)
    pie_chart_data = {dept['department']: dept['voters'] for dept in department_data}

    # Prepare data for Bar Chart (Department comparison of voters and candidates)
    bar_chart_labels = [dept['department'] for dept in department_data]
    bar_chart_voters = [dept['voters'] for dept in department_data]
    bar_chart_candidates = [dept['candidates'] for dept in department_data]

    # Prepare data for Line Graph (Comparing Voters vs Votes)
    voters_count = Voter.objects.count()
    total_votes = Voter.objects.exclude(voted_candidate=None).count()  # Number of voters who cast votes

    line_graph_data = {
        'labels': ['Total Voters', 'Votes Cast'],
        'values': [voters_count, total_votes]
    }

    # Fetch the logged-in user's profile
    profile = get_object_or_404(AdminProfile, user=request.user)

    # Check if the request is an AJAX request using the X-Requested-With header
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Return JSON data for AJAX request
        return JsonResponse({
            'department_data': department_data,
            'pie_chart_data': pie_chart_data,
            'bar_chart_labels': bar_chart_labels,
            'bar_chart_voters': bar_chart_voters,
            'bar_chart_candidates': bar_chart_candidates,
            'line_graph_data': line_graph_data,
        })

    # If not AJAX, render the full page
    context = {
        'department_data': department_data,
        'pie_chart_data': pie_chart_data,
        'bar_chart_labels': bar_chart_labels,
        'bar_chart_voters': bar_chart_voters,
        'bar_chart_candidates': bar_chart_candidates,
        'line_graph_data': line_graph_data,
        'profile': profile,  # Pass profile to template
    }
    return render(request, 'reports.html', context)







@login_required
def update_profile(request):
    user = request.user

    # Check if profile exists
    profile, created = AdminProfile.objects.get_or_create(user=user)

    if request.method == "POST":
        address = request.POST.get("address")
        city = request.POST.get("city")
        institution = request.POST.get("institution")

        # Update profile fields
        profile.address = address
        profile.city = city
        profile.institution = institution

        if "profile_picture" in request.FILES:
            profile.profile_picture = request.FILES["profile_picture"]

        profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("dashboard")  # Redirect to the admin panel after updating

    return render(request, "admin_panel.html", {"profile": profile})


