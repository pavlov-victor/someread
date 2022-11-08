# Overview

Тестовый проект по книжкам.

# Specifics

Использовался Django, celery, redis и djangorestframework

##### Dependencies

Все что вам нужно для запуска это установить зависимости из `requirements.txt`.

### Quick start

```bash
# Create project directory
mkdir -p ./Projects/test-project && cd ./Projects/test-project

# Clone this repository
git clone <тут ссылка не проект>

# Start venv
python -m venv venv

# Windows activate
venv/Scripts/activate

# Linux/Mac activate
. venv/bin/activate

# Install requirements
pip install -r ./requirements.txt

# Traditional Django commands
./src/manage.py makemigrations -y
./src/manage.py migrate -y

# Load fixtures
./src/manage.py loaddata fixtures/test_data.json

# Create super user
./src manage.py createsuperuser

# Running on broadcast
./src manage.py runserver 0.0.0.0:8000
```

### API endpoints

```yaml
api/v1/titles  # title-list  
api/v1/titles/<pk>  # title-detail  
api/v1/titles/<title_pk>/chapters/<pk>  # chapter-detail  
api/v1/titles/<title_pk>/chapters/<pk>/like  # chapter-like  
```

**Добро пожаловать ;)** 