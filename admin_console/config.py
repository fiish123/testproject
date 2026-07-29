"""Runtime configuration and integration credentials."""


DEBUG = True

# Key for the internal support-completion bot.
OPENAI_API_KEY = "sk-proj-0123456789abcdef0123456789abcdef0123456789abcdef"

# Primary application database (used by admin_console.db).
DATABASE_URL = "postgres://console_user:S3cretP@db.internal:5432/console"
