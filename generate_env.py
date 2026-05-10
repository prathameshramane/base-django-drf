import yaml
import os

def flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}".upper() if parent_key else k.upper()
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def generate_env(public_yaml_path='env.public.yaml', private_yaml_path='env.private.yaml', env_out_path='.env'):
    env_vars = {}

    if os.path.exists(public_yaml_path):
        with open(public_yaml_path, 'r') as f:
            public_vars = yaml.safe_load(f)
            if public_vars:
                env_vars.update(flatten_dict(public_vars))

    if os.path.exists(private_yaml_path):
        with open(private_yaml_path, 'r') as f:
            private_vars = yaml.safe_load(f)
            if private_vars:
                # Merge logic - if key overlaps, private overrides.
                env_vars.update(flatten_dict(private_vars))

    # Construct COMPOSE_PROFILES based on USE_*
    profiles = ['web']
    if str(env_vars.get('USE_POSTGRES', '')).lower() == 'true':
        profiles.append('postgres')
    if str(env_vars.get('USE_REDIS', '')).lower() == 'true':
        profiles.append('redis')
    if str(env_vars.get('USE_CELERY', '')).lower() == 'true':
        profiles.append('celery')

    env_vars['COMPOSE_PROFILES'] = ','.join(profiles)

    with open(env_out_path, 'w') as f:
        for key, value in env_vars.items():
            f.write(f"{key}={value}\n")
    print(f"Generated {env_out_path} successfully.")

if __name__ == '__main__':
    generate_env()
