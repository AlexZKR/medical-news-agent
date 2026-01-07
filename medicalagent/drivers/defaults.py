"""Default values and initial state for the Medical News Agent application."""

# Application Settings
DEFAULT_SETTINGS = {
    "date_range": "Last Month",
    "strict_mode": True,
}

# Trusted Sources
DEFAULT_TRUSTED_SOURCES = [
    "nakedscience.ru",
    "statnews.com",
    "medscape.com",
    "medicalnewstoday.com",
]

# UI State Defaults
DEFAULT_UI_STATE = {
    "active_dialog_id": 1,
    "init": True,
}

# Welcome Message
DEFAULT_WELCOME_MESSAGE = {
    "role": "assistant",
    "content": "Hello! I'm your Medical Research Agent. Try 'Find latest diabetes news'.",
}

# New Dialog Placeholder
NEW_DIALOG_PLACEHOLDER = {
    "id": None,  # Will be set dynamically
    "title": "New Research Discussion",
}

# Dialog Switch Messages

# New Dialog Welcome Message
NEW_DIALOG_WELCOME_MESSAGE = {
    "role": "assistant",
    "content": "Hello! I'm your Medical Research Agent. What would you like to research today?",
}
