import os
import json
import time
import requests
from django.utils.log import AdminEmailHandler
from copy import copy
from django.conf import settings
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()


# Bot_OAuth_Token = 'xoxb-2271343814839-3816656868517-FNkzLTm3yflIRJzE5mE7l6IB'
class SlackLoggerHandler(AdminEmailHandler):
    def emit(self, record, *args, **kwargs):
        try:
            request = record.request
            subject = "%s (%s IP): %s" % (
                record.levelname,
                (
                    "internal"
                    if request.META.get("REMOTE_ADDR") in settings.INTERNAL_IPS
                    else "EXTERNAL"
                ),
                record.getMessage(),
            )
        except Exception:
            subject = "%s: %s" % (record.levelname, record.getMessage())
            request = None
        subject = self.format_subject(subject)

        # Since we add a nicely formatted traceback on our own, create a copy
        # of the log record without the exception data.
        no_exc_record = copy(record)
        no_exc_record.exc_info = None
        no_exc_record.exc_text = None

        if record.exc_info:
            exc_info = record.exc_info
        else:
            exc_info = (None, record.getMessage(), None)

        reporter = self.reporter_class(request, is_email=True, *exc_info)
        message = "%s\n\n%s" % (
            self.format(no_exc_record),
            reporter.get_traceback_text(),
        )
        html_message = reporter.get_traceback_html() if self.include_html else None
        slack_message_block = {
            "attachments": [
                {
                    "color": "#f2c744",
                    "blocks": [
                        {
                            "type": "header",
                            "text": {
                                "type": "plain_text",
                                "text": "New request",
                            }
                        },
                        {
                            "type": "section",
                            "fields": [
                                {
                                    "type": "mrkdwn",
                                    "text": "*Type:*\nPaid Time Off"
                                },
                                {
                                    "type": "mrkdwn",
                                    "text": "*Created by:*\n<example.com|Fred Enriquez>"
                                }
                            ]
                        },
                        {
                            "type": "section",
                            "fields": [
                                {
                                    "type": "mrkdwn",
                                    "text": "*When:*\nAug 10 - Aug 13"
                                },
                                {
                                    "type": "mrkdwn",
                                    "text": "*Type:*\nPaid time off"
                                }
                            ]
                        },
                        {
                            "type": "section",
                            "fields": [
                                {
                                    "type": "mrkdwn",
                                    "text": "*Hours:*\n16.0 (2 days)"
                                },
                                {
                                    "type": "mrkdwn",
                                    "text": "*Remaining balance:*\n32.0 hours (4 days)"
                                }
                            ]
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": "<https://example.com|View request>"
                            }
                        }
                    ]
                }
            ]
        }
        main_text = 'Error at ' + time.strftime("%A, %d %b %Y %H:%M:%S +0000", time.gmtime())
        split = 7900
        parts = range(math.ceil(len(message.encode('utf8')) / split))

        for part in parts:
            start = 0 if part == 0 else split * part
            end = split if part == 0 else split * part + split

            # combine final text and prepend it with line breaks
            # so the details in slack message will fully collapse
            detail_text = '\r\n\r\n\r\n\r\n\r\n\r\n\r\n' + message[start:end]

            slack_message_block.append({
                'color': 'danger',
                'title': 'Details (Part {})'.format(part + 1),
                'text': detail_text,
                'ts': time.time(),
            })
        channel = 'C027ZA3Q22K'
        # data = {
        #     'payload': json.dumps({'main_text': main_text, 'attachments': slack_message_block}),
        # }
        # r = requests.post(
        #     url=slack_chat_url,
        #     data=data,
        #     headers={"Authorization": f"{os.environ.get('SLACK_BOT_TOKEN')}"}
        # )
        # os.environ.get('SLACK_BOT_TOKEN')
        main_text = 'Error at ' + time.strftime("%A, %d %b %Y %H:%M:%S +0000", time.gmtime())

        a = {
            "channel": "C027ZA3Q22K",
            "attachments": [
                {
                    "mrkdwn_in": ["type"],
                    "color": "#36a64f",
                    "pretext": "Optional pre-text that appears above the attachment block",
                    "author_name": 'askldglkasndgljnasdkjgna',
                    "author_link": "http://flickr.com/bobby/",
                    "author_icon": "https://placeimg.com/16/16/people",
                    "title": "title",
                    "title_link": "https://api.slack.com/",
                    "text": "Optional `text` that appears within the attachment",
                    "fields": [
                        {
                            "title": "A field's title",
                            "value": "This field's value",
                            "short": 'false'
                        },
                        {
                            "title": "A short field's title",
                            "value": "A short field's value",
                            "short": 'true'
                        },
                        {
                            "title": "A second short field's title",
                            "value": "A second short field's value",
                            "short": 'true'
                        }
                    ],
                    "thumb_url": "http://placekitten.com/g/200/200",
                    "footer": "footer",
                    "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
                    "ts": 123456789
                }
            ]
        }
        # construct data
        data = {
            'payload': json.dumps({
                'main_text': main_text,
                'attachments': a}),
        }
        data1 = {
            'payload': json.dumps({
                "channel": "C027ZA3Q22K",
                "attachments": [
                    {
                        "fallback": "Plain-text summary of the attachment.",
                        "color": "#2eb886",
                        "pretext": "Optional text that appears above the attachment block",
                        "author_name": "Bobby Tables",
                        "author_link": "http://flickr.com/bobby/",
                        "author_icon": "http://flickr.com/icons/bobby.jpg",
                        "title": "Slack API Documentation",
                        "title_link": "https://api.slack.com/",
                        "text": "Optional text that appears within the attachment",
                        "fields": [
                            {
                                "title": "Priority",
                                "value": "High",
                                "short": 'false'
                            }
                        ],
                        "image_url": "http://my-website.com/path/to/image.jpg",
                        "thumb_url": "http://example.com/path/to/thumb.png",
                        "footer": "Slack API",
                        "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
                        "ts": 123456789
                    }
                ]
            }),
        }
        slack_chat_url = 'https://slack.com/api/chat.postMessage'

        # send it
        r = requests.post(slack_chat_url, data=data,
                          headers={'Authorization': 'Bearer xoxb-2271343814839-3816656868517-FNkzLTm3yflIRJzE5mE7l6IB'})
        # curl - X
        # POST - F
        # channel = C027ZA3Q22K - F
        # text = "Reminder: we've got a softball game tonight"
        # https: // slack.com / api / chat.postMessage - H
        # "Authorization: Bearer xoxb-2271343814839-3816656868517-FNkzLTm3yflIRJzE5mE7l6IB"


c = {"blocks": [
    {
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": "New request",
        }
    },
    {
        "type": "section",
        "fields": [
            {
                "type": "mrkdwn",
                "text": "*Type:*\nPaid Time Off"
            },
            {
                "type": "mrkdwn",
                "text": "*Created by:*\n<example.com|Fred Enriquez>"
            }
        ]
    },
    {
        "type": "section",
        "fields": [
            {
                "type": "mrkdwn",
                "text": "*When:*\nAug 10 - Aug 13"
            },
            {
                "type": "mrkdwn",
                "text": "*Type:*\nPaid time off"
            }
        ]
    },
    {
        "type": "section",
        "fields": [
            {
                "type": "mrkdwn",
                "text": "*Hours:*\n16.0 (2 days)"
            },
            {
                "type": "mrkdwn",
                "text": "*Remaining balance:*\n32.0 hours (4 days)"
            }
        ]
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "<https://example.com|View request>"
        }
    }
]}
