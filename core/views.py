from django.shortcuts import render, get_object_or_404
from .models import Asignatura, ProfesorAsignatura
from face_reco.recognizer import generate_video_stream
from django.http import StreamingHttpResponse

def clase_view(request, asignatura_id):
    asignatura = get_object_or_404(Asignatura, pk=asignatura_id)
    profesores = ProfesorAsignatura.objects.filter(asignatura=asignatura)

    return render(request, 'core/clase.html', {
        'asignatura': asignatura,
        'profesores': profesores,
    })

def video_feed(request):
    return StreamingHttpResponse(generate_video_stream(), content_type='multipart/x-mixed-replace; boundary=frame')

def elegir_clase(request):
    asignaturas = Asignatura.objects.all()
    return render(request, 'core/elegir_clase.html', {'asignaturas': asignaturas})
