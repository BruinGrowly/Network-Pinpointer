#!/usr/bin/env python3
"""
Alert Integration - Send alerts to external systems

Supports:
- Slack webhooks
- Email (SMTP)
- Generic webhooks
- File logging
"""

import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Optional, List
from datetime import datetime
from pathlib import Path
import requests


class AlertManager:
    """Manages alerts to external systems"""

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.alert_log = Path(self.config.get('alert_log', './network_alerts.log'))

    def send_alert(
        self,
        title: str,
        message: str,
        severity: str = "INFO",
        details: Optional[Dict] = None
    ):
        """
        Send alert to all configured channels

        Args:
            title: Alert title
            message: Alert message
            severity: CRITICAL, HIGH, MEDIUM, LOW, INFO
            details: Additional context
        """
        alert_data = {
            'timestamp': datetime.now().isoformat(),
            'title': title,
            'message': message,
            'severity': severity,
            'details': details or {}
        }

        # Log to file always
        self._log_to_file(alert_data)

        # Send to configured channels
        if self.config.get('slack_webhook'):
            self._send_to_slack(alert_data)

        if self.config.get('email'):
            self._send_email(alert_data)

        if self.config.get('webhook'):
            self._send_webhook(alert_data)

    def _log_to_file(self, alert_data: Dict):
        """Log alert to file"""
        self.alert_log.parent.mkdir(parents=True, exist_ok=True)

        with open(self.alert_log, 'a') as f:
            f.write(json.dumps(alert_data) + '\n')

    def _send_to_slack(self, alert_data: Dict):
        """Send alert to Slack"""
        webhook_url = self.config.get('slack_webhook')

        if not webhook_url:
            return

        # Map severity to color
        color_map = {
            'CRITICAL': '#d32f2f',
            'HIGH': '#f57c00',
            'MEDIUM': '#fbc02d',
            'LOW': '#388e3c',
            'INFO': '#1976d2'
        }

        color = color_map.get(alert_data['severity'], '#757575')

        # Build Slack message
        slack_message = {
            'attachments': [{
                'color': color,
                'title': f"[{alert_data['severity']}] {alert_data['title']}",
                'text': alert_data['message'],
                'footer': 'Network Pinpointer',
                'ts': int(datetime.now().timestamp())
            }]
        }

        # Add details if present
        if alert_data['details']:
            fields = []
            for key, value in alert_data['details'].items():
                fields.append({
                    'title': key.replace('_', ' ').title(),
                    'value': str(value),
                    'short': True
                })
            slack_message['attachments'][0]['fields'] = fields

        try:
            response = requests.post(webhook_url, json=slack_message, timeout=10)
            if response.status_code != 200:
                print(f"Slack alert failed: {response.status_code}")
        except Exception as e:
            print(f"Failed to send Slack alert: {e}")

    def _send_email(self, alert_data: Dict):
        """Send alert via email"""
        email_config = self.config.get('email', {})

        if not email_config:
            return

        try:
            msg = MIMEMultipart()
            msg['From'] = email_config.get('from', 'network-pinpointer@localhost')
            msg['To'] = email_config.get('to')
            msg['Subject'] = f"[{alert_data['severity']}] {alert_data['title']}"

            # Build email body
            body = f"""
Network Pinpointer Alert

Severity: {alert_data['severity']}
Time: {alert_data['timestamp']}

{alert_data['message']}

"""

            if alert_data['details']:
                body += "\nDetails:\n"
                for key, value in alert_data['details'].items():
                    body += f"  {key}: {value}\n"

            msg.attach(MIMEText(body, 'plain'))

            # Send email
            smtp_server = email_config.get('smtp_server', 'localhost')
            smtp_port = email_config.get('smtp_port', 587)

            with smtplib.SMTP(smtp_server, smtp_port) as server:
                if email_config.get('use_tls', True):
                    server.starttls()

                if email_config.get('username'):
                    server.login(
                        email_config['username'],
                        email_config.get('password', '')
                    )

                server.send_message(msg)

        except Exception as e:
            print(f"Failed to send email alert: {e}")

    def _send_webhook(self, alert_data: Dict):
        """Send to generic webhook"""
        webhook_url = self.config.get('webhook')

        if not webhook_url:
            return

        try:
            response = requests.post(webhook_url, json=alert_data, timeout=10)
            if response.status_code not in [200, 201, 202]:
                print(f"Webhook alert failed: {response.status_code}")
        except Exception as e:
            print(f"Failed to send webhook alert: {e}")


if __name__ == "__main__":
    # Demo alert system
    config = {
        'alert_log': './demo_alerts.log',
        # 'slack_webhook': 'https://hooks.slack.com/services/YOUR/WEBHOOK/URL',
        # 'email': {
        #     'from': 'network@example.com',
        #     'to': 'admin@example.com',
        #     'smtp_server': 'smtp.gmail.com',
        #     'smtp_port': 587,
        #     'username': 'your-email@gmail.com',
        #     'password': 'your-password'
        # }
    }

    manager = AlertManager(config)

    # Test alert
    manager.send_alert(
        title="Network Performance Degraded",
        message="Power dimension dropped from 0.85 to 0.45",
        severity="HIGH",
        details={
            'target': 'api.example.com',
            'love': 0.85,
            'power': 0.45,
            'impact': '47% performance drop'
        }
    )

    print("✓ Alert sent (check ./demo_alerts.log)")
