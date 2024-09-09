# Flask API Boilerplate

_The README is auto generated by an AI_

## Prerequisites

Before starting, create a `.env` file in the root folder. You can find the required environment variables in `env_example.txt` and modify them as needed.

## First-Time Setup

To start the app for the first time, run the following command in the root folder:

```bash
docker-compose up --build
```

### Initial Values and Seeding

Adding initial values to your database can be done from the commands/seeding section. By executing these commands you can insert pre defined values to your tables when needed.

If you need to to execute multiple seeding steps when running your application for the first time, the `run-init-seeders.sh` script can be utilized. Follow as started by adding new seeding steps. To execute teh script itself just run `bash ./scripts/run-init-seeders.sh` command from the project root. If you are using windows you will need to do this from the wsl/bash terminal instead from cmd/powershell.

## Documentation

OpenAPI docs are available when the server is started, they can be viewed my going to `http://localhost:5000/` in your browser.

The docs should be updated by following the current setup in the schemas folder.

## Database Setup and Migrations

### CLI Commands

Note: For any `docker exec` command to run, ensure the Docker container is up and running.

- **Create a migration:**

  ```bash
  docker exec backend flask db:create-migration --name <migration_name>
  ```

- **Run migrations:**

  ```bash
  docker exec backend flask db:migrate [--single]
  ```

- **Rollback migrations:**

  ```bash
  docker exec backend flask db:rollback [--steps <n>]
  ```

- **Check migration status:**
  ```bash
  docker exec backend flask db:migrate-status
  ```

### Migration Workflow

1. Pull the latest code.
2. Run migrations to ensure the database schema is up to date.
3. Backend developers create, test, and push migration files. These changes are included in pull requests.
4. On production, migrations are applied automatically after code deployment.

## Project Setup

### Initial Setup

1. **Bring down services:**

   ```bash
   docker-compose down
   ```

2. **Remove old database volume:**

   ```bash
   docker volume rm development_postgresdata
   ```

3. **Delete old migration files:**

   ```bash
   sudo rm -rf migrations
   ```

4. **Pull the latest code and bring up services:**

   ```bash
   git pull origin develop && docker-compose up -d --build
   ```

5. **Run migrations:**
   ```bash
   docker exec backend flask db:migrate
   ```

## Code Structure

- **Models:** Use `BaseModel` as a parent class for all database models (e.g., `UserProfile`).
- **Tasks:** Asynchronous tasks are located in the `tasks` folder. These tasks are run using Celery, with Redis as the broker.
- **Validators:** Use `BaseValidator` as a parent class for new validators.
- **Config:** The `BaseConfig` is extended by `AppConfig`. Follow this structure for any new configurations.
- **Logging:** All logging is configured in the `logs` folder. Adjust the logger setup to add new workflows if needed.
- **Commands:** Backend testing commands such as health checks and migrations are in the `commands` folder.
- **Storage:** Temporary storage for user files is in the `storage` folder.

## Updating Migrations

Whenever you modify the database (e.g., adding, editing, or removing a model), create a new migration using the steps above to keep the database schema up to date.

## Accessing the App

Once the app is running, the backend will be available at `localhost:5000`.
