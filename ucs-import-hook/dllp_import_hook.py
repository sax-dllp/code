from ucsschool.importer.exceptions import InitialisationError
from ucsschool.importer.models.import_user import ImportUser
from ucsschool.importer.utils.user_pyhook import UserPyHook
from univention.config_registry import ConfigRegistry

ucr = ConfigRegistry()
ucr.load()

class DLLPAutomation(UserPyHook):
    priority = {
        "pre_create": 100,
    }

    async def pre_create(self, obj: ImportUser) -> None:
        await self.set_props(obj)

    async def set_props(self, user):
        school = user.school
        self.logger.info("DLLP - User belongs to school: %r", school)
    
        role_translation = {
            "student": "schueler",
            "teacher": "lehrer",
            "staff": "mitarbeiter"
        }

        # Read config
        role_name = role_translation.get(user.roles[0], user.roles[0])
        self.logger.info("DLLP - User belongs to role: %r", role_name)

        quota = ucr.get(f'DLLP/{school}/users/{role_name}/ox/quota')
        self.logger.info("DLLP - Set quota to: %r", quota)

        ox_enabled = ucr.get(f'DLLP/{school}/users/{role_name}/ox/enabled')
        self.logger.info("DLLP - Set ox_enabled to: %r", ox_enabled)

        ox_context = ucr.get(f'DLLP/{school}/users/{role_name}/ox/context')
        self.logger.info("DLLP - Set ox_context to: %r", ox_context)

        ms_enabled = ucr.get(f'DLLP/{school}/users/{role_name}/ms365/enabled')
        self.logger.info("DLLP - Set ms_enabled to: %r", ms_enabled)

        connection_alias = ucr.get(f'DLLP/{school}/users/{role_name}/ms365/connection_alias')
        self.logger.info("DLLP - Set connection_alias to: %r", connection_alias)

        # Plausi checks
        if ox_enabled == 'true' or ms_enabled == 'true':
            if user.email is None:
                raise InitialisationError("DLLP - OX or MS enabled, but email address missing")

        if ox_enabled == 'true':
            if ox_context is None:
                raise InitialisationError("DLLP - OX enabled, but no ox context is set")

        if ms_enabled == 'true':
            if connection_alias is None:
                raise InitialisationError("DLLP - MS365 enabled, but no connection alias is set")

        # Alter user object
        if quota is not None:
            user.udm_properties['mailUserQuota'] = int(quota)

        if ox_enabled is not None and ox_enabled == 'true':
            user.udm_properties['isOxUser'] = ox_enabled.lower() == 'true'

        if ox_context is not None:
            user.udm_properties['oxContext'] = int(ox_context)

        if ms_enabled is not None and ms_enabled == 'true':
            user.udm_properties['UniventionOffice365Enabled'] = ms_enabled.lower() == 'true'

        if connection_alias is not None:
            user.udm_properties['UniventionOffice365ADConnectionAlias'] = [connection_alias]

        self.logger.info("DLLP - Hook finished successfully")
