import yaml
import os

def prompt_yes_no(question, default="no"):
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        print(question + prompt, end='')
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            print("Please respond with 'yes' or 'no' (or 'y' or 'n').")

def main():
    print("Welcome to the Django Scaffold Configuration Script!")
    print("This will configure your env.public.yaml.\n")

    use_postgres = prompt_yes_no("Do you want to use PostgreSQL?", default="yes")
    use_redis = prompt_yes_no("Do you want to use Redis?", default="yes")
    use_celery = prompt_yes_no("Do you want to use Celery?", default="yes")

    config = {
        "DEBUG": "True",
        "USE_POSTGRES": "True" if use_postgres else "False",
        "USE_REDIS": "True" if use_redis else "False",
        "USE_CELERY": "True" if use_celery else "False"
    }

    if use_postgres:
        config["POSTGRES_DB"] = "postgres"
        config["POSTGRES_USER"] = "postgres"
        config["POSTGRES_PASSWORD"] = "postgres"
        config["POSTGRES_HOST"] = "postgres"
        config["POSTGRES_PORT"] = "5432"

    if use_redis:
        config["REDIS_URL"] = "redis://redis:6379/1"

    if use_celery:
        config["CELERY_BROKER_URL"] = "redis://redis:6379/0"
        config["CELERY_RESULT_BACKEND"] = "redis://redis:6379/0"

    with open("env.public.yaml", "w") as f:
        yaml.dump(config, f, default_flow_style=False)

    print("\nConfiguration saved to env.public.yaml.")
    print("Run `python generate_env.py` to update your .env file.")

if __name__ == "__main__":
    main()
