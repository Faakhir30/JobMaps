from django.http import JsonResponse
from django.shortcuts import render
from .models import Job
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def index(request):
    return render(request,f'JobMap/index.html')

def figuresAPI(request):
    return JsonResponse({'job':Job.objects.count(),
                         'firms':Job.objects.values('company').distinct().count()+5,
                         'cities':int(Job.objects.values('location').distinct().count()*.8)},
                           status=201)

@csrf_exempt
def discriptionAPI(request, id):
    if request.method=='POST':
        print(id, Job.objects.first())
        job=Job.objects.get(id=id)
        print(job)
        return JsonResponse({
            'title':job.title,'discription':job.discription,'link':job.apply,'company':job.company,
            'companyLN':job.company_linkedIn,'applyLN':job.apply_linkedIn,"location":job.location,
        },status=201)