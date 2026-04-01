test:
	uv run python manage.py test

install:
	uv sync

build:
	./build.sh

createadmin:
	uv run python manage.py createsuperuser

start:
	uv run gunicorn task_manager.wsgi --bind 0.0.0.0:${PORT}

dev:
	uv run python manage.py runserver 0.0.0.0:${PORT}

check:
	uv run ruff check

all-test:
	make test
	make check

render-start:
	gunicorn task_manager.wsgi --bind 0.0.0.0:${PORT}

collectstatic:
	python manage.py collectstatic --noinput

ci-migrate:
	uv run python manage.py makemigrations --noinput && \
    	uv run python manage.py migrate --noinput

migrate:
	uv run python manage.py migrate

PORT ?= 8000
