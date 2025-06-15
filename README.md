# Веб-приложения движения денежных средств


## Запуск

Проект сделан на Sqlite, поэтому запускается без настройки бд

```bash
  git clone https://github.com/NikUvolen/tech-task
  cd tech-task
  python -m venv venv
  . ./venv/bin/activate
  pip install -r requirements.txt
  python CashFlow/manage.py migrate
  python CashFlow/manage.py runserver
```

## Скрины

![wecome_page](screens/welcome_page.png)

![main_page](screens/main_page.png)

![main_page_filter](screens/main_page_filter.png)

![add_transaction_page.png](screens/add_transaction_page.png)

![update_transaction_page.png](screens/update_transaction_page.png)

![md_page.png](screens/md_page.png)

![md_update_page.png](screens/md_update_page.png)

![md_delete_page.png](screens/md_update_page.png)