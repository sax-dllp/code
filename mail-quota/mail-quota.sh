#!/usr/bin/env bash

###################################################################
# Mail Quota Report                                               #
# 1. Collects data from all contexts in CSV format                #
# 2. Uses Python script to modify and order CSV                   #
# 3. For each context, total quota usage and limit are calculated #
# 4. Generates CSV report                                         #
###################################################################

# Debugging: print every line that is executed
set -x
# Exit on error, unset variable and pipe fail.
set -euo pipefail

CSV_INPUT="data.csv"
CSV_SORTED="data-sorted.csv"
CSV_REPORT="mail-quota-$(date +"%Y-%m-%d").csv"

get_quota() {
    local domain=$1
    local column=$2

    if [ "$2" = "usage" ]; then
        column=5
    elif [ "$2" = "limit" ]; then
        column=6
    else
        echo "Invalid argument. Please use 'usage' or 'limit'."
        return 1
    fi

    # Get quota table for domain and sum specified column
    local sum=$(doveadm -f table quota get -u "*@$domain" | \
        grep STORAGE | \
        awk -v column="$column" '{sum += $column} END {print sum}')

    # Set sum to 0 if empty
    [[ -z "$sum" ]] && sum=0

    echo "$sum"
}

convert() {
    local input=$1

    # Convert KB in GB
    echo "scale=2; $input / (1024 * 1024)" | \
            bc | \
            xargs printf "%.2f"
}


# Get data for all contexts
/opt/open-xchange/sbin/listcontext -A oxadminmaster -P \
    $(< /etc/ox-secrets/master.secret) --csv |
    # Ignore first two lines (header and context 10)
    # and write 8th column to CSV_INPUT
    awk -F '"' 'NR>2 { print $16; }' > "$CSV_INPUT"

# Modify CSV_INPUT
# - delete context*
# - move context id to first column
# - write to CSV_SORTED
python3 modify-csv.py $CSV_INPUT $CSV_SORTED

# Write header for CSV_REPORT
echo "Context ID,Quota-Nutzung in GB,Quota-Limit in GB" > "$CSV_REPORT"

# Reading CSV_SORTED line by line
while IFS=',' read -r line; do
    # Extract first field from comma-separated list
    id=$(echo "$line" | cut -d ',' -f 1)
    # Extract everything after first field from comma-separated list
    domainlist=$(echo "$line" | cut -d ',' -f 2-)

    usage_sum=0
    limit_sum=0

    # Read domainlist into array
    IFS=',' read -ra domains <<< "$domainlist"
    # Get quota for each domain and add to sum
    for domain in "${domains[@]}"; do
        # remove carriage return
        tr_domain=$(echo "$domain" | tr -d '\r')

        usage_add=$(get_quota "$tr_domain" usage)
        usage_sum=$((usage_sum + usage_add  ))
        limit_add=$(get_quota "$tr_domain" limit)
        limit_sum=$((limit_sum + limit_add))
    done

    # Convert KB in GB
    usage_sum=$(convert "$usage_sum")
    limit_sum=$(convert "$limit_sum")

    # Append id, usage and limit to CSV_REPORT
    echo "$id,$usage_sum,$limit_sum" >> "$CSV_REPORT"

done < "$CSV_SORTED"

# Clean up
rm $CSV_INPUT
rm $CSV_SORTED

echo "Script execution complete. Output written to $CSV_REPORT"
