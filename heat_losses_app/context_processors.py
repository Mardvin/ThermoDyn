def left_menu(request):
    return {
        'left_menu': [
            {'title': 'Результаты расчетов', 'url_name': 'result'},
            {'title': 'Расчет тепловой мощности', 'url_name': 'heat_power'},
            {'title': 'Расчет тепловых потерь', 'url_name': 'heat_losses'},
            {'title': 'Расчет потерь через изоляцию', 'url_name': 'losses_insulation'},
        ]
    }