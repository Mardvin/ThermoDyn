def left_menu(request):
    return {
        'left_menu': [
            {'title': 'Результаты расчетов', 'url_name': 'result'},
            {'title': 'Расчет тепловой мощности', 'url_name': 'heat_power_home'},
            {'title': 'Расчет тепловых потерь', 'url_name': 'heat_losses'},
            {'title': 'Расчет потерь через изоляцию', 'url_name': 'losses_insulation'},
            {'title': 'Расчет затрат электроэнергии', 'url_name': 'electricity_costs'},
        ]
    }

def up_menu(request):
    return {
        'menu': [
            {'title': "О сайте", 'url_name': 'heat_power_home'},
            {'title': "Константы", 'url_name': 'heat_power_home'},
            {'title': "Войти", 'url_name': 'heat_power_home'},
        ]
    }