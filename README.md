# AuthDjangoRestFramework
собственная система аутентификации и авторизации

## Схема базы данных

### accounts_user
- `id` – primary key
- `email` – уникальный, используется для входа
- `password` – хеш bcrypt (60 символов)
- `name`, `surname`, `patronymic` – имя, фамилия, отчество
- `role_id` – внешний ключ на `roles_permissions_role`
- `is_active` – мягкое удаление (False = аккаунт заблокирован)

### roles_permissions_role
- `id`
- `name` – уникальное название роли (admin, manager, user, guest)
- `description` – описание

### roles_permissions_resource
- `id`
- `name` – уникальное название ресурса (article, comment, user)
- `description`

### roles_permissions_permission
- `id`
- `role_id` – внешний ключ на Role
- `resource_id` – внешний ключ на Resource
- `can_create`, `can_read`, `can_update`, `can_delete` – базовые CRUD-права
- `can_read_all`, `can_update_all`, `can_delete_all` – права на все объекты данного типа
- Уникальность пары (role, resource)

## Основные эндпоинты

| Метод | URL | Описание |
|-------|-----|----------|
| POST | /api/register/ | Регистрация нового пользователя |
| POST | /api/login/ | Вход |
| POST | /api/logout/ | Выход |
| GET | /api/articles/ | Список статей |

## Проверка прав

Реализована функция `check_permission` в `roles_permissions/utils.py`. Логика:
1. Если у роли есть all-право (например, `can_read_all`), доступ к любым объектам.
2. Иначе проверяется базовое право и принадлежность объекта пользователю (по полю `owner_id`).

Пример: админ может выполнить мягкое удаление любого пользователя (`can_delete_all=True`), обычный пользователь – только себя (`can_delete_all=False`, `can_delete=True`).

## Тестовые пользователи

| email | пароль | роль |
|-------|--------|------|
| admin@example.com | admin123 | admin |
| manager@example.com | manager123 | manager |
| user@example.com | user123 | user |
| guest@example.com | guest123 | guest |

## Технологии
- Python 3.12.2
- Django + Django REST Framework
- JWT (PyJWT) для аутентификации
- bcrypt для хеширования паролей
- SQLite
