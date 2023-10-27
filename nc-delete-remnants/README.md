# delete_remnants
Get a list of remnant ldap users that have not logged in since time x and optionally delete or deactivate them

You **can** pass options to the script, but you don't have to.

Default values are:
| option | default value |
| - | - |
| action | display |
| directory | /var/www/nextcloud |
| output | plain |
| row | detected |
| time | 1 year |
| user | www-data |

:warning::warning: **WARNING**: Actions "disable" and "delete" will be executed immediately on all matching users and you will not get asked to confirm them! :warning::warning:

```
Usage: delete_remnants.sh [OPTIONS]
OPTIONS includes:
                -a | --action   - Select what to do to users [display,disable,delete]		Default: display
                -d | --dir      - Define Nextcloud directory. Must be in double quotes		Default: /var/www/nextcloud
                -h | --help     - Show this help text
                -o | --output   - Select output format [plain,csv,quiet]			Default: plain
                -q | --quiet    - Disable output (same as -o quiet)
	        -r | --row      - Define which date row to evaluate. [login,detected]		Default: detected
				  login: evaluates last login date
				  detected: evaluates the date on which the user was marked as remnant
                -t | --time     - Define maximum time since last login (e.g. 1 year)		Default: 1 year
                                  Valid time formats are: 
                                        X second(s)
                                        X minute(s)
                                        X hour(s)
                                        X day(s)
                                        X week(s)
                                        X month(s)
                                        X year(s)
                -u | --user     - Define the user who's executing the web server		Default: www-data
```
