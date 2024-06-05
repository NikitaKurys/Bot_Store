import os


# Выгрузка логов покупок
async def get_buy_logs_gettr(**kwargs):
    path_buy_logs = "user_logs/buy_logs"
    dir_list = os.listdir(path_buy_logs)
    logs = []

    for log in dir_list:
        if os.path.getsize(f'{path_buy_logs}/{log}') != 0:
            logs.append(
                (
                    os.path.getsize(f'{path_buy_logs}/{log}'), log,
                )
            )

    return {'buy_logs': logs}


# Выгрузка логов сабскрайберов
async def get_subscribers_logs_gettr(**kwargs):
    path_subscribers_logs = "user_logs/subscribers_logs"
    dir_list = os.listdir(path_subscribers_logs)
    logs = []

    for log in dir_list:
        if os.path.getsize(f'{path_subscribers_logs}/{log}') != 0:
            logs.append(
                (
                    os.path.getsize(f'{path_subscribers_logs}/{log}'), log,
                )
            )

    return {'subscribers_logs': logs}
