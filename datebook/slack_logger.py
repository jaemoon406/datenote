import json
import requests
import math

from django.utils.timezone import now
from django.utils.log import AdminEmailHandler
from django.views.debug import ExceptionReporter
from django.conf import settings
from datebook.settings import common

from copy import copy
# Bot_OAuth_Token = 'xoxb-2271343814839-3816656868517-FNkzLTm3yflIRJzE5mE7l6IB'

class SlackLoggerHandler(AdminEmailHandler):
    def emit(self, record):
        try:
            request = record.request
            subject = '%s (%s IP): %s' % (
                record.levelname,
                ('internal' if request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS else 'EXTERNAL'),
                record.getMessage())
        except Exception:
            subject = '%s: %s' % (record.levelname, record.getMessage())
            request = None
        subject = self.format_subject(subject)
        no_exc_record = copy(record)
        no_exc_record.exc_info = None
        no_exc_record.exc_text = None

        if record.exc_info:
            exc_info = record.exc_info
        else:
            exc_info = (None, record.getMessage(), None)
        reporter = ExceptionReporter(request, is_email=True, *exc_info)
        message = "%s\n\n%s" % (self.format(no_exc_record), reporter.get_traceback_text())
        html_message = reporter.get_traceback_html() if self.include_html else None

        # 위 코드는 기본 admin_email handler의 emit
        slack_channel_name = 'django-test'
        print(common.SLACK_BOT_TOKEN)
        slack_token = 'Bearer ' + common.SLACK_BOT_TOKEN

        if request:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'{slack_token}'
            }

            attachments_blocks = [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "Server Error",
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*Type :*\n{record.levelname}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Created by :*\n{now()}"
                        }
                    ]
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*Path :*\n {request.path if request else 'None'}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Method : *\n {request.method if request else 'None'}"
                        }
                    ]
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*Status Code :*\n {record.status_code if request else 'None'}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*User :*\n {request.user if request else 'None'}"
                        },
                    ]
                },
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"Error Code :\n"
                    }
                },
                {
                    "type": "divider"
                },
            ]

            error_text = record.exc_text.encode('utf8') if record.exc_text else None
            # 오늘자 slack 최대 글자 수 3001
            maximum_char = 2500
            if error_text is None:
                return None
            else:
                for i in range(math.ceil(len(error_text) / maximum_char)):
                    start = i * maximum_char + i
                    end = i * maximum_char + maximum_char + i

                    sliced_error_text = error_text[start:end].decode()
                    error_code = {
                        'text': {
                            'text': f'```{sliced_error_text}```',
                            'type': 'mrkdwn'},
                        'type': 'section'
                    }
                    attachments_blocks.append(error_code)

                attachments_blocks.append({'type': 'divider'})
                payload = {'attachments': [
                    {'blocks': attachments_blocks,
                     'color': '#E54646'}
                ], 'channel': f'{slack_channel_name}'}

                r = requests.post('https://slack.com/api/chat.postMessage',
                                  headers=headers,
                                  data=json.dumps(payload)
                                  )
        else:
            pass
