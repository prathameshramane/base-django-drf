import yaml

def prompt_yes_no(question, default="yes"):
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
        "debug": True,
        "use": {
            "postgres": use_postgres,
            "redis": use_redis,
            "celery": use_celery
        }
    }

    if use_postgres:
        config["postgres"] = {
            "db": "postgres",
            "user": "postgres",
            "password": "postgres",
            "host": "postgres",
            "port": 5432
        }

    if use_redis:
        config["redis"] = {
            "url": "redis://redis:6379/1"
        }

    if use_celery:
        config["celery"] = {
            "broker_url": "redis://redis:6379/0",
            "result_backend": "redis://redis:6379/0"
        }

    with open("env.public.yaml", "w") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    print("\nConfiguration saved to env.public.yaml.")
    print("Run `python generate_env.py` to update your .env file.")

if __name__ == "__main__":
    main()
