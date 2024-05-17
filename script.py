from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoClip
import numpy as np


def create_frame(
        t: float, text: str, font: ImageFont.FreeTypeFont,
        text_width: int, text_height: int, video_width: int,
        video_height: int, duration: int) -> np.ndarray:
    """Создаёт кадр."""
    # Создаем новое черное изображение
    img = Image.new('RGB', (video_width, video_height), color='black')
    draw = ImageDraw.Draw(img)

    # Вычисляем позицию текста, для прокрутки через экран за 'duration' секунд
    total_distance = video_width + text_width + 15  # Чтобы полностью скрылся
    x = video_width - int(total_distance * (t / duration))
    y = (video_height - text_height) // 2  # Центрируем текст по вертикали

    # Рисуем текст на изображении
    draw.text((x, y), text, font=font, fill='white')

    # Конвертируем изображение в кадр
    return np.array(img)


def generate_scrolling_text_video(text: str, output_file: str) -> None:
    """Генерирует MP4 видео с прокручивающимся текстом."""
    # Размеры видео
    video_width, video_height = 100, 100
    duration = 3  # секунды
    fps = 60  # кадры в секунду

    # Загружаем шрифт по умолчанию
    font = ImageFont.truetype("DejaVuSans.ttf", 20)

    # Создаем временное изображение для вычисления размеров текста
    dummy_img = Image.new('RGB', (video_width, video_height))
    draw = ImageDraw.Draw(dummy_img)
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # Создаем видеоклип покадрово
    video_clip = VideoClip(
        lambda t: create_frame(
            t, text, font, text_width, text_height,
            video_width, video_height, duration
            ), duration=duration
        )

    # Устанавливаем количество кадров в секунду
    video_clip = video_clip.set_fps(fps)

    # Записываем видео в файл
    video_clip.write_videofile(output_file, codec='libx264')


if __name__ == "__main__":
    text = "От топота копыт, пыль по полю летит!"
    output_file = "scrolling_text.mp4"
    generate_scrolling_text_video(text, output_file)
