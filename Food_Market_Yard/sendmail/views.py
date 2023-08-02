from datetime import datetime

from django.core.mail import EmailMultiAlternatives  # импортируем класс для создание объекта письма с html
from django.shortcuts import render, redirect
from django.template.loader import render_to_string  # импортируем функцию, которая срендерит наш html в текст
from django.views import View

from .models import Appointment


class AppointmentView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'make_appointment.html', {})

    def post(self, request, *args, **kwargs):
        date_str = request.POST.get('date')  # Получаем значение по ключу 'date', если оно есть
        client_name = request.POST.get('client_name')
        message = request.POST.get('message')
        appointment = None

        if date_str and client_name and message:
            # Проверяем, что все необходимые данные присутствуют
            appointment = Appointment(
                date=datetime.strptime(date_str, '%Y-%m-%d'),
                client_name=client_name,
                message=message,
            )
            appointment.save()

        # получаем наш html
        html_content = render_to_string(
            'appointment_created.html',
            {
                'appointment': appointment,
            }
        )

        # в конструкторе уже знакомые нам параметры, да? Называются правда немного по другому, но суть та же.
        msg = EmailMultiAlternatives(
            subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}',
            body=appointment.message,  # это то же, что и message
            from_email='Djangopython.org@yandex.ru',
            to=['imrontursunov@gmail.com'],  # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html
        msg.send()  # отсылаем

        return redirect('appointments:make_appointment')