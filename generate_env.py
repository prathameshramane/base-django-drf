import yaml
import os

def generate_env(public_yaml_path='env.public.yaml', private_yaml_path='env.private.yaml', env_out_path='.env'):
    env_vars = {}

    if os.path.exists(public_yaml_path):
        with open(public_yaml_path, 'r') as f:
            public_vars = yaml.safe_load(f)
            if public_vars:
                env_vars.update(public_vars)

    if os.path.exists(private_yaml_path):
        with open(private_yaml_path, 'r') as f:
            private_vars = yaml.safe_load(f)
            if private_vars:
                env_vars.update(private_vars)

    with open(env_out_path, 'w') as f:
        for key, value in env_vars.items():
            f.write(f"{key}={value}\n")
    print(f"Generated {env_out_path} successfully.")

if __name__ == '__main__':
    generate_env()
