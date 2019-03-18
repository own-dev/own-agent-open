# === Settings configurations
META_SECTION_KEY = 'meta'
SERVICE_SECTION_KEY = 'service'
CONTENT_SECTION_KEY = 'content'

ID_KEY = 'id'
CAPACITY_KEY = 'capacity'
SALARY_KEY = 'salary'
CURRENCY_KEY = 'currency'
SUBSCRIPTION_INTERVAL_COUNT_KEY = 'subscriptionIntervalCount'

SUBSCRIPTION_INTERVAL_KEY = 'subscriptionInterval'
SUBSCRIPTION_PLANS_KEY = 'agentSubscriptionPlans'
PLAN_PRICINGS_KEY = 'agentSubscriptionPlanPricings'
SUBSCRIPTION_PLAN_OWNER_TYPE_KEY = 'agentSubscriptionPlanOwnerType'
SUBSCRIPTION_SECTION_KEY = 'subscription'
OWNER_TYPE_USER = 'USER'
OWNER_TYPE_ORG = 'ORGANIZATION'
DAY_KEY = 'DAY'
DAY_CAPACITY_KEY = 'day_capacity'
DAY_SALARY_KEY = 'day_salary'
DAY_INTERVAL_KEY = 'day_interval_count'
WEEK_KEY = 'WEEK'
WEEK_CAPACITY_KEY = 'week_capacity'
WEEK_SALARY_KEY = 'week_salary'
WEEK_INTERVAL_KEY = 'week_interval_count'
MONTH_KEY = 'MONTH'
MONTH_CAPACITY_KEY = 'month_capacity'
MONTH_SALARY_KEY = 'month_salary'
MONTH_INTERVAL_KEY = 'month_interval_count'
YEAR_KEY = 'YEAR'
YEAR_CAPACITY_KEY = 'year_capacity'
YEAR_SALARY_KEY = 'year_salary'
YEAR_INTERVAL_KEY = 'year_interval_count'

DEFAULT_PERIOD_TIME_FOR_UPDATES_CHECKER = 150  # in seconds

# 'production' env var is lead to send logs to google cloud platform
PRODUCTION_ENVIRONMENT = 'production'
GOOGLE_LOGGER_NAME = 'agents-platform'

# Local logger's levels
DEBUG_LEVEL = 'Debug'
INFO_LEVEL = 'Info'
WARNING_LEVEL = 'Warning'
ERROR_LEVEL = 'Error'
EXCEPTION_LEVEL = 'Exception'

# Google logger has 'CRITICAL' level instead 'EXCEPTION'
# Mapping of local logger levels to the ones of Google's
google_logger_enums = {
    DEBUG_LEVEL: 'DEBUG',
    INFO_LEVEL: 'INFO',
    WARNING_LEVEL: 'WARNING',
    EXCEPTION_LEVEL: 'ERROR',
    ERROR_LEVEL: 'CRITICAL'
}

HTML_REF_CODE = 'application/vnd.uberblik.htmlReference'

NUM_THREADS_PER_SERVICE = 5
NUMBER_OF_TASKS_KEY = 'num_tasks'

# CLI
FILENAME_KEY = 'filename'
