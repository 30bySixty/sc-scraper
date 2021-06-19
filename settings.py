import os

SLACK_TOKEN = os.getenv('SLACK_TOKEN')

# SLACK_CHANNEL = "#housing"
SLACK_CHANNEL = "#test2"

SLEEP_INTERVAL = 20 * 60 # 20 minutes
# SLEEP_INTERVAL = 1 * 10 # 20 minutes <- debug

## Search preferences
CRAIGSLIST_SITE = 'sfbay'

AREA = "scz"

# The maximum rent you want to pay per month.
MAX_PRICE = 4000

ZIP_CODES = [
	95060, #SC
	95062, #SC
	95063, #SC
	95064, #SC
	95001, #aptos
	95003, #aptos
	95010, #capitola
	95062, #capitola
	95073, #soquel
	95076 #watsonville
]

# Discarded zip codes:
# 95061 <- too far into forests
# 95064 <- too close to UCSC
# 95065 <- too far into forests
# 95066 <- scotts valley, too far into forests and shitty
# 95067 <- scotts valley
# 95019 <- watsonville near the airport
# 95077 <- internal watsonville
