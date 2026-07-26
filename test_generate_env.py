import unittest
import tempfile
import os
import yaml
from generate_env import flatten_dict, generate_env

class TestGenerateEnv(unittest.TestCase):

    def test_flatten_dict_basic(self):
        d = {'a': 1, 'b': 2}
        expected = {'A': 1, 'B': 2}
        self.assertEqual(flatten_dict(d), expected)

    def test_flatten_dict_nested(self):
        d = {'a': {'b': {'c': 1}}, 'd': 2}
        expected = {'A_B_C': 1, 'D': 2}
        self.assertEqual(flatten_dict(d), expected)

    def test_flatten_dict_empty(self):
        self.assertEqual(flatten_dict({}), {})

    def test_generate_env_logic(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            public_yaml_path = os.path.join(tmpdir, 'env.public.yaml')
            private_yaml_path = os.path.join(tmpdir, 'env.private.yaml')
            env_out_path = os.path.join(tmpdir, '.env')

            # Public vars
            public_vars = {
                'use': {'postgres': True, 'redis': False, 'celery': True},
                'secret': 'public_secret',
                'app': {'name': 'MyApp'}
            }
            with open(public_yaml_path, 'w') as f:
                yaml.dump(public_vars, f)

            # Private vars
            private_vars = {
                'secret': 'private_secret',
                'use': {'redis': True}
            }
            with open(private_yaml_path, 'w') as f:
                yaml.dump(private_vars, f)

            generate_env(public_yaml_path, private_yaml_path, env_out_path)

            self.assertTrue(os.path.exists(env_out_path))

            # Read back .env
            env_vars = {}
            with open(env_out_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and '=' in line:
                        key, val = line.split('=', 1)
                        env_vars[key] = val

            # Verify overrides and flattening
            self.assertEqual(env_vars.get('SECRET'), 'private_secret')
            self.assertEqual(env_vars.get('APP_NAME'), 'MyApp')

            self.assertEqual(env_vars.get('USE_POSTGRES'), 'True')
            self.assertEqual(env_vars.get('USE_REDIS'), 'True')
            self.assertEqual(env_vars.get('USE_CELERY'), 'True')

            # COMPOSE_PROFILES
            self.assertEqual(env_vars.get('COMPOSE_PROFILES'), 'web,postgres,redis,celery')

    def test_generate_env_no_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            public_yaml_path = os.path.join(tmpdir, 'missing_public.yaml')
            private_yaml_path = os.path.join(tmpdir, 'missing_private.yaml')
            env_out_path = os.path.join(tmpdir, '.env')

            generate_env(public_yaml_path, private_yaml_path, env_out_path)

            self.assertTrue(os.path.exists(env_out_path))
            with open(env_out_path, 'r') as f:
                content = f.read().strip()
                self.assertEqual(content, 'COMPOSE_PROFILES=web')

    def test_generate_env_empty_yaml_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            public_yaml_path = os.path.join(tmpdir, 'empty_public.yaml')
            private_yaml_path = os.path.join(tmpdir, 'empty_private.yaml')
            env_out_path = os.path.join(tmpdir, '.env')

            with open(public_yaml_path, 'w') as f:
                pass # empty file
            with open(private_yaml_path, 'w') as f:
                pass # empty file

            generate_env(public_yaml_path, private_yaml_path, env_out_path)

            self.assertTrue(os.path.exists(env_out_path))
            with open(env_out_path, 'r') as f:
                content = f.read().strip()
                self.assertEqual(content, 'COMPOSE_PROFILES=web')

if __name__ == '__main__':
    unittest.main()
