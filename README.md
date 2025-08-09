---
# Ticket Management System

This project implements a **dynamic roles and permissions system** mapped to resources and actions, built with Django and Django REST Framework. It also includes Tailwind CSS setup for possible template-based UI.
---

## Deliverables

- **Django ReST Framework** for API development
- **Django** for backend development
- **Django REST Framework Simple JWT** for JWT authentication
- **DRF-Spectacular** for API documentation
- **Django Admin** customization for ease of use and security
- **Example seed data** as managed commands for initial setup
- **README.md** for project documentation and instructions
- **Basic TestCases** for models and auth endpoint
- **Dockerfile** for containerization
- **Tailwind CSS** for styling

## Getting Started

Follow these steps to set up and run the system locally:

1. **Clone the repo and checkout the branch:**

   ```bash
   git clone https://github.com/prakashtaz0091/Ticket-Management-System.git
   cd Ticket-Management-System
   git checkout permissions-mapped-to-actions
   ```

2. **Create and activate a Python virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

3. **Install required packages:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations:**

   ```bash
   python manage.py migrate
   ```

5. **Seed the database with initial data:**

   This command will set up default actions, example roles, users, statuses, and priorities:

   ```bash
   python manage.py seed_example_data
   ```

   _Note:_ This command internally calls other commands like `set_actions`, `set_example_roles_users`, and `set_example_status_priorities` to automate setup. **`set_actions`** command is mandatory to run. Don't want example data? Run

   ```bash
   python manage.py set_actions
   ```

   and you are ready to use the system.

6. **Run the development server:**

   ```bash
   python manage.py runserver
   ```

7. **Access the system at:**

   ```
   http://127.0.0.1:8000/
   http://127.0.0.1:8000/admin/
   http://127.0.0.1:8000/swagger-ui/
   http://127.0.0.1:8000/redoc/
   ```

---

## How the System Works

[See the ER/UML diagram](./erd.pdf)

### Dynamic Roles and Permissions

- The core feature is **dynamic roles and permissions** where both roles and permissions can be named and created freely as per your needs, no hardcoded permission names.

### Permissions are Linked to Actions and Resources

- Permissions are tied to **actions**, and actions are tied to **resources**.

- In this system **Resources** include:

  - `menu-level1`
  - `menu-level2`
  - `menu-level3`
  - `ticket`
  - `status`
  - `priorities`
  - `user-menu-assignments`

- ModelViewset **actions** include default CRUD plus others like:

  - `create`
  - `list`
  - `update`
  - `destroy`
  - `retrieve`
  - Non-default/custom actions like `get_assigned_menus`, `get_assigned_tickets` for restricted access (user can only see the menus/tickets assigned to them).

- Actions are **created automatically** by the `set_actions` management command and **cannot be modified manually** in the admin to ensure consistency.

---

## Role-Based Permission Handling

Role-based permission checking is implemented dynamically by matching user roles, permissions, and actions tied to resources.

```python
def has_permission(user, resource_to_access, action_to_perform):
    if not user.is_authenticated:
        return False
    try:
        role = user.profile.role
    except Exception as e:
        logger.warning(f"User profile or role error: {e}")
        return False
    else:
        permissions = role.permissions.prefetch_related("actions").all()
        for permission in permissions:
            if f"{resource_to_access}:{action_to_perform}" in permission.actions_list:
                return True
        return False


class RoleBasedPermission(BasePermission):
    def has_permission(self, request, view):
        resource = view.basename
        action = view.action
        return has_permission(
            request.user, resource_to_access=resource, action_to_perform=action
        )
```

- The `has_permission` function checks if the authenticated user’s role has a permission containing the combined `"resource:action"` string.
- `RoleBasedPermission` is a DRF permission class that extracts the current view’s resource and action, then delegates the check to `has_permission`.
- This design enables fully dynamic role and permission assignment without hardcoding permission names in backend code.

---

## Notes

- Tailwind CSS is set up and ready to use in case you want to build template-based UI.

- The system is designed with flexibility so you can extend it with new roles, permissions, resources, and actions without touching backend code.

---

## Optional: Running with Docker

You can run the project in a containerized environment using Docker:

1. **Build the Docker image:**

   ```bash
   docker build -t ticket-management-system .
   ```

2. **Run the Docker container (exposes port 8000):**

   ```bash
   docker run -p 8000:8000 ticket-management-system
   ```

3. **Access the system at:**

   ```
   http://127.0.0.1:8000/
   http://127.0.0.1:8000/admin/
   http://127.0.0.1:8000/swagger-ui/
   http://127.0.0.1:8000/redoc/
   ```

---
