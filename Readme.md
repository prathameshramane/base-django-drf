# Run Using different environments

This project can be used to switch between developement and production settings.

## Activating different environments

- Development environment

  > python manage.py runserver --settings=backend.settings.development

- Production environment
  > python manage.py runserver --settings=backend.settings.production

# Adding environment variables

- Declare variable in .env file
  > TEST_VARIABLE = 'TEST_VALUE'
- Use the variable value using
  > config('TEST_VARIABLE')
  > eg. EMAIL_HOST_USER = config('EMAIL_HOST_USER')
