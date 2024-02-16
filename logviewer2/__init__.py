import os

import sentry_sdk
from sentry_sdk.integrations.excepthook import ExcepthookIntegration
from sentry_sdk.integrations.flask import FlaskIntegration

from logviewer2.utils import GET_REV

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN", None),
    release=GET_REV(),
    integrations=[FlaskIntegration(), ExcepthookIntegration(always_run=True)],
    traces_sample_rate=1.0
)