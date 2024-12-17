from azure.communication.email import EmailClient
from azure.core.exceptions import HttpResponseError

def send_confirmation_email(to_email, confirm_url):
    # Ваш Connection String из Azure
    connection_string = "endpoint=https://emailverification.europe.communication.azure.com/;accesskey=5AmtnaiV7QFEFai8chBBuvjfILWL1UjlwID9btaCJh2vRAz5JtsdJQQJ99AJACULyCp3TOYfAAAAAZCSxhkP"

    # Создаем клиента для отправки писем
    email_client = EmailClient.from_connection_string(connection_string)

    # Тема и тело письма
    subject = 'Подтверждение регистрации'
    body = f'Пожалуйста, подтвердите вашу регистрацию, перейдя по ссылке: {confirm_url}'

    # Параметры для отправки письма
    message = {
        "content": {
            "subject": subject,
            "plainText": body,
        },
        "recipients": {
            "to": [
                {"address": to_email}
            ]
        },
        # Используем подтвержденного отправителя
        "senderAddress": "DoNotReply@ba47d0de-c058-47ac-8e7b-a9a693a45d09.azurecomm.net"
    }

    try:
        # Отправляем письмо
        poller = email_client.begin_send(message)
        result = poller.result()  # Ожидаем завершения отправки
        print(f"Результат отправки письма: {result}")  # Выводим весь результат для отладки
    except HttpResponseError as ex:
        print(f"Ошибка при отправке письма: {ex}")