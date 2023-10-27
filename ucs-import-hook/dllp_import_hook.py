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
    
        role_translation = {
        "student": "schueler",
        "teacher": "lehrer",
        "staff": "mitarbeiter"
        
        }
        role_name = role_translation.get(user.roles[0], user.roles[0])
        quota = ucr.get(f'DLLP/{school}/users/{role_name}/ox/quota')
        ox_enabled = ucr.get(f'DLLP/{school}/users/{role_name}/ox/enabled')
        ms_enabled = ucr.get(f'DLLP/{school}/users/{role_name}/ms365/enabled')
        connection_alias = ucr.get(f'DLLP/{school}/users/{role_name}/ms365/connection_alias')
        if quota is not None:
            user.udm_properties['mailUserQuota'] = int(quota)
        if ox_enabled is not None and ox_enabled == 'true':
            user.udm_properties['isOxUser'] = ox_enabled.lower() == 'true'
        if ms_enabled is not None and ms_enabled == 'true':
            user.udm_properties['UniventionOffice365Enabled'] = ms_enabled.lower() == 'true'
        if connection_alias is not None:
            user.udm_properties['UniventionOffice365ADConnectionAlias'] = [connection_alias]
