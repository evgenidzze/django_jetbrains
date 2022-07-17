from django.shortcuts import render, redirect
from django.views import View
from django.http.response import HttpResponse
from collections import deque


class WelcomeView(View):
    @staticmethod
    def get(request, *args, **kwargs):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')


class MenuView(View):
    template_name = 'tickets/menu.html'
    context = {'Change oil': 'change_oil',
               'Inflate tires': 'inflate_tires',
               'Get diagnostic test': 'diagnostic'}

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'context': self.context})


line_of_cars = {'change_oil': deque(), 'inflate_tires': deque(), 'diagnostic': deque()}
num = 0
wait_time = 0


class GetTicket(View):
    @staticmethod
    def get(request, service):
        template_name = 'tickets/get_ticket.html'
        global num, wait_time
        num += 1
        if service == 'change_oil':
            wait_time = len(line_of_cars[service]) * 2
        elif service == 'inflate_tires':
            wait_time = len(line_of_cars['change_oil']) * 2 + len(line_of_cars[service]) * 5
        elif service == 'diagnostic':
            wait_time = len(line_of_cars['change_oil']) * 2 + len(line_of_cars['inflate_tires']) * 5 + len(
                line_of_cars[service]) * 30
        line_of_cars[service].append({'num': num, 'time': wait_time})
        return render(request, template_name, {'ticket': line_of_cars[service][-1]})


ticket_num = None


def processing(request):
    """Показує чергу кожного типу обслуговування, при натисканні кнопки,
    видаляє лівого клієнта"""
    global line_of_cars
    global ticket_num
    template_name = 'tickets/processing.html'
    queue_len = {'oil': len(line_of_cars['change_oil']),
                 'tires': len(line_of_cars['inflate_tires']),
                 'diagnostic': len(line_of_cars['diagnostic'])}
    if request.method == 'POST':
        ticket_num = None
        for service in line_of_cars:
            if line_of_cars[service]:
                ticket = line_of_cars[service].popleft()
                ticket_num = ticket['num']
                return redirect('/next')
        return redirect('/next')
    return render(request, template_name, {'queue_len': queue_len})


class NextPage(View):
    def get(self, request):
        template_name = 'tickets/next.html'
        return render(request, template_name, {'ticket_num': ticket_num})
