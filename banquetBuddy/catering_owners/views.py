from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from core.models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from .forms import EmployeeFilterForm, CateringProfileForm

# Create your views here.

@login_required
def employee_applications(request, offer_id):
    
    offer = get_object_or_404(Offer, id=offer_id)
    
    if request.user != offer.cateringservice.cateringcompany.user:
        return render(request, 'error.html', {'message': 'No tienes permisos para acceder a esta oferta'})
    
    applicants = offer.job_applications.select_related('employee').all()

    filter_form = EmployeeFilterForm(request.GET or None)
    if filter_form.is_valid():
        applicants = filter_form.filter_queryset(applicants)

    context = {'applicants': applicants, 'offer': offer, 'filter_form': filter_form}
    return render(request, "applicants_list.html", context)

@login_required
def catering_profile_edit(request):
    context = {}
    user = request.user

    # Obtener el perfil de la empresa de catering del usuario actual
    catering_company = CateringCompany.objects.get_or_create(user=user)[0]

    if request.method == "POST":
        form = CateringProfileForm(request.POST, request.FILES, instance=catering_company)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado exitosamente")
            return redirect("profile")
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")
    else:
        form = CateringProfileForm(instance=catering_company)

    context["form"] = form
    return render(request, "profile_company_edit.html", context)