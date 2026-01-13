import os

import streamlit as st


def load_secrets_into_env() -> None:
    """
    Bridge function: Loads Streamlit secrets into os.environ
    so Pydantic Settings and LangChain can see them.
    """

    if hasattr(st, "secrets"):
        for key, value in st.secrets.items():
            # Streamlit secrets can be nested (tables), strictly speaking
            # environment variables are flat strings.
            # We only load top-level string/int values.
            if isinstance(value, str | int | float):
                os.environ[key] = str(value)
