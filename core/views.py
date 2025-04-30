from django.shortcuts import render
from django.http import StreamingHttpResponse
from face_reco.recognizer import generate_video_stream



def video_feed(request):
    return StreamingHttpResponse(generate_video_stream(), content_type='multipart/x-mixed-replace; boundary=frame')


def stream_page(request):
    return render(request, 'core/stream.html')
