from django.http import FileResponse, HttpResponse
from django.shortcuts import redirect, render

from .forms import TextForm
from .utils import generate_video_script
from .models import Video
import urllib.parse


def homepage(request):
    if request.method == 'POST':
        form = TextForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            return redirect(f'/runtext/?text={text}')
    else:
        form = TextForm()

    return render(request, 'homepage.html', {'form': form})


def generate_video(request):
    if 'text' in request.GET:
        text = request.GET['text']
        # Кодирование текста для использования в имени файла
        encoded_text = urllib.parse.quote(text)
        # Проверка на наличие текста в базе данных
        try:
            video = Video.objects.get(text=text)
            response = FileResponse(open(video.video_file.path, 'rb'), content_type='video/mp4')
            response['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'{encoded_text}.mp4'
            return response
        except Video.DoesNotExist:
            # Генерация видео
            output_file = f'media/videos/{text}.mp4'
            generate_video_script(text, output_file)

            # Сохранение видео в базе данных
            video = Video.objects.create(text=text, video_file=output_file)
            video.save()

            # Отправка видеофайла в ответ на запрос
            response = FileResponse(open(video.video_file.path, 'rb'), content_type='video/mp4')
            response['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'{encoded_text}.mp4'
            return response
    else:
        return HttpResponse('Добавьте параметр text. "?text=<ваш текст>"')
