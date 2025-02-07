from django.shortcuts import render, get_object_or_404
from .models import User
import pdfkit
from django.http import HttpResponse
from django.template import loader

# Create your views here.

def accept(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        summary = request.POST.get('summary', '')
        degree = request.POST.get('degree', '')
        school = request.POST.get('school', '')
        university = request.POST.get('university', '')
        previous_work = request.POST.get('previous_work', '')
        skills = request.POST.get('skills', '')

        user = User(name=name, email=email, phone=phone, summary=summary, degree=degree, school=school, university=university, previous_work=previous_work, skills=skills)
        user.save()

        return render(request, 'pdf/accept.html')
    else:
        return render(request, 'pdf/accept.html')

def resume(request, id):
    profile_user = User.objects.get(pk=id)
    template = loader.get_template('pdf/resume.html')
    html = template.render({'profile_user': profile_user})

    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
    }

    # Explicitly provide wkhtmltopdf path
    config = pdfkit.configuration(wkhtmltopdf=r"C:\wkhtmltox\bin\wkhtmltopdf.exe")

    try:
        pdf = pdfkit.from_string(html, False, options=options, configuration=config)
    except OSError as e:
        return HttpResponse(f"Error generating PDF: {str(e)}", status=500)

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment'
    filename = "resume.pdf"
    return response

def listing(request):
    users = User.objects.all()
    return render(request, 'pdf/list.html', {'users': users})

