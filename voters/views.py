
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from staff.models import Voter, Candidate
import re
from django.contrib import messages


################HOME PAGE##############
def voting(request):
    return render(request, 'voting.html')

from django.contrib.auth import logout

def logout_voter(request):
    logout(request)
    return redirect('voting')  # Redirect to the login page or homepage after logout





def authenticate_voter(request):
    if request.method == 'POST':
        adm_no = request.POST.get('adm_no')
        voter_code = request.POST.get('voter_code')

        try:
            voter = Voter.objects.get(reg_number=adm_no, voter_code=voter_code)

            # Store voter details in session
            request.session['voter_name'] = voter.name
            request.session['voter_code'] = voter.voter_code
            request.session['voter_department'] = voter.department

           
            return redirect('voter_page')  # Redirect to the voting dashboard
        except Voter.DoesNotExist:
            messages.error(request, "Invalid Admission Number or Voter Code.")
    
    return render(request, 'auth.html')


# Mapping of voter code prefixes to departments
DEPARTMENT_CODES = {
    "AF": "Accounting & Finance",
    "BA": "Business Administration & Management",
    "ES": "Economics & Statistics",
    "SD": "Software Development & Information",
    "AC": "Applied Computing & Network",
    "EP": "Education & Physical Studies",
    "PA": "Performing Arts, Film, Media & Economic Studies",
}

def voter_page(request):
    voter_code = request.session.get("voter_code")

    if not voter_code:
       
        return redirect("authenticate_voter")

    # Extract department prefix from voter code
    match = re.match(r"([A-Z]+)", voter_code)
    department_name = DEPARTMENT_CODES.get(match.group(1)) if match else None

    # Get voter object
    voter = get_object_or_404(Voter, voter_code=voter_code)

    # Fetch candidates for the department
    candidates = Candidate.objects.filter(department=department_name) if department_name else Candidate.objects.none()

    return render(request, "template.html", {"candidates": candidates, "voter": voter})

def vote(request, candidate_id):
    voter_code = request.session.get("voter_code")

    if not voter_code:
        messages.error(request, "You must be logged in to vote.")
        return redirect("authenticate_voter")

    voter = get_object_or_404(Voter, voter_code=voter_code)

    if voter.voted_candidate:
        messages.error(request, "You have already voted! Unvote first to change your vote.")
        return redirect("voter_page")

    candidate = get_object_or_404(Candidate, id=candidate_id)

    # Increment vote count
    candidate.votes += 1
    candidate.save()

    # Assign the voted candidate to the voter
    voter.voted_candidate = candidate
    voter.save()

    messages.success(request, f"You have successfully voted for {candidate.name}.")
    return redirect("voter_page")

def unvote(request, candidate_id):
    voter_code = request.session.get("voter_code")

    if not voter_code:
        messages.error(request, "You must be logged in to un-vote.")
        return redirect("authenticate_voter")

    voter = get_object_or_404(Voter, voter_code=voter_code)

    if not voter.voted_candidate or voter.voted_candidate.id != candidate_id:
        messages.error(request, "You cannot un-vote for a candidate you haven't voted for!")
        return redirect("voter_page")

    candidate = voter.voted_candidate

    # Reduce the vote count (ensure it doesn’t go below zero)
    if candidate.votes > 0:
        candidate.votes -= 1
        candidate.save()

    # Remove the voted candidate
    voter.voted_candidate = None
    voter.save()

    messages.success(request, "You have successfully removed your vote.")
    return redirect("voter_page")
