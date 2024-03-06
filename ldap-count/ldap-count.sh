#!/usr/bin/env bash

##############################################################
# LDAP CSV Report                                            #
#   Mitarbeiter-, Lehrer-, Schüleranzahl für jeden Mandanten #
##############################################################

# Debugging: print every line that is executed
#set -x
# Exit on error.
set -o errexit
# Exit on error inside any functions or subshells.
set -o errtrace
# Do not allow use of undefined vars.
set -o nounset
# Catch error in case pipe fails
set -o pipefail


# LDAP server information
LDAP_BASE="$(ucr get ldap/base)"
echo "LDAP base: $LDAP_BASE"

# CSV file
CSV="ldap-count-$(date +"%Y-%m-%d").csv"


# Function to perform univention-ldapsearch for each user type, and append counts to CSV
perform_ldapsearch() {
  local ou=$1
  local target_csv_file=$2

  # LDAP queries
  LDAP_QUERY_MITARBEITER="cn=mitarbeiter,cn=users,ou=$ou,$LDAP_BASE"
  LDAP_QUERY_LEHRER="cn=lehrer,cn=users,ou=$ou,$LDAP_BASE"
  LDAP_QUERY_SCHUELER="cn=schueler,cn=users,ou=$ou,$LDAP_BASE"

  # Run univention-ldapsearch for each query
  mitarbeiter_count=$(univention-ldapsearch -b "$LDAP_QUERY_MITARBEITER" | grep "^cn:" | wc -l)
  lehrer_count=$(univention-ldapsearch -b "$LDAP_QUERY_LEHRER" | grep "^cn:" | wc -l)
  schueler_count=$(univention-ldapsearch -b "$LDAP_QUERY_SCHUELER" | grep "^cn:" | wc -l)

  # Append counts to CSV
  echo "$ou,$mitarbeiter_count,$lehrer_count,$schueler_count" >> "$target_csv_file"
}


# OU_Array contains Mandanten
declare -a OU_ARRAY=()
# Run the command and read each line into the array
while read -r line; do
    OU_ARRAY+=("$line")
done < <(univention-ldapsearch -b $LDAP_BASE "objectclass=ucsschoolOrganizationalUnit" | grep "^ou:" | awk '{print $2}')


# Print count and array
echo "Mandantenanzahl: ${#OU_ARRAY[@]}"
printf '%s\n' "${OU_ARRAY[@]}"

# Create CSV file with headers
echo "Mandant,Mitarbeiter,Lehrer,Schüler" > "$CSV"

# Loop through each OU, perform univention-ldapsearch
for ou in "${OU_ARRAY[@]}"; do
  perform_ldapsearch "$ou" "$CSV"
done

echo "CSV file created: $CSV"

# Display formatted CSV file
column -t -s, < "$CSV" | less -S
