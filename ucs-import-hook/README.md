# DLLP Automation Hook for UCS@school Kelvin REST API

This Python script is a hook for the UCS@school Kelvin REST API. It's designed to automate the setting of properties for users based on their roles and schools. The properties are set before the user is created (pre_create), and are sourced from the Univention Configuration Registry (UCR).

## Installation

1. Place the `dllp_import_hook.py` file in the `/var/lib/ucs-school-import/kelvin-hooks` directory on your UCS@school server.

2. Set the required UCR variables.

3. Restart the Kelvin REST API service for the changes to take effect:

```
/etc/init.d/docker-app-ucsschool-kelvin-rest-api restart
```

## Usage

The hook will automatically run whenever a user is created via the Kelvin REST API. It will set properties for the user based on their role (student, teacher, or staff) and school. The properties are sourced from the UCR and include settings for Open-Xchange (OX) and Microsoft 365.

## Updating

If you make changes to the hook or set new UCR variables, you will need to restart the Kelvin REST API service for the changes to take effect:

```
/etc/init.d/docker-app-ucsschool-kelvin-rest-api restart
```
