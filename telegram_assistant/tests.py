from django.test import TestCase, Client
from unittest.mock import patch, MagicMock
from . import utils
from django.urls import reverse
import requests
from pathlib import Path

class UtilsTests(TestCase):
    def test_mask_token_typical(self):
        token = '123456789:ABCdefGHIjklMNOpqrSTUvwxyz'
        masked = utils.mask_token(token)
        self.assertIn(':', masked)
        self.assertNotEqual(masked, token)
        self.assertTrue(masked.startswith('123456'))
        self.assertTrue(masked.endswith(token[-3:]))

    def test_mask_token_none(self):
        self.assertIsNone(utils.mask_token(None))

    def test_mask_token_unexpected_format(self):
        token = 'abcdefghi1234567'
        masked = utils.mask_token(token)
        self.assertNotEqual(masked, token)
        self.assertTrue(masked.startswith('abcdef'))
        self.assertTrue(masked.endswith(token[-3:]))

    @patch.object(Path, "exists", return_value=True)
    def test_check_env_file_exists(self, mock_exists):
        self.assertTrue(utils.check_env_file())

    @patch('telegram_assistant.utils.requests.get')
    def test_is_ngrok_running_true(self, mock_get):
        mock_get.return_value.status_code = 200
        self.assertTrue(utils.is_ngrok_running())

    @patch('telegram_assistant.utils.requests.get', side_effect=requests.exceptions.RequestException)
    def test_is_ngrok_running_false(self, mock_get):
        self.assertFalse(utils.is_ngrok_running())

class MonitorViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    @patch('telegram_assistant.views.is_ngrok_running', return_value=False)
    @patch('telegram_assistant.views.check_env_file', return_value=False)
    def test_monitor_view_get(self, mock_env, mock_ngrok):
        response = self.client.get(reverse('telegram_assistant:monitor'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('ngrok_running', response.context)
        self.assertIn('env_exists', response.context)

    @patch('telegram_assistant.views.is_ngrok_running', return_value=True)
    @patch('telegram_assistant.views.get_ngrok_url', return_value='https://test.ngrok.io')
    @patch('telegram_assistant.views.check_env_file', return_value=True)
    @patch('telegram_assistant.views.get_telegram_token', return_value='123456789:ABCdefGHIjklMNOpqrSTUvwxyz')
    @patch('telegram_assistant.views.mask_token', return_value='123456*:ABCD****xyz')
    @patch('telegram_assistant.views.validate_telegram_token', return_value=(True, 'testbot'))
    @patch('telegram_assistant.views.get_bot_detailed_info', return_value={'id': 1, 'username': 'testbot'})
    def test_monitor_view_context(self, mock_info, mock_valid, mock_mask, mock_token, mock_env, mock_url, mock_ngrok):
        response = self.client.get(reverse('telegram_assistant:monitor'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['ngrok_running'])
        self.assertEqual(response.context['ngrok_url'], 'https://test.ngrok.io')
        self.assertTrue(response.context['env_exists'])
        self.assertTrue(response.context['token_exists'])
        self.assertTrue(response.context['token_valid'])
        self.assertEqual(response.context['token_message'], 'testbot')
        self.assertEqual(response.context['bot_info']['username'], 'testbot')

class CheckStatusViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    @patch('telegram_assistant.views.is_ngrok_running', return_value=True)
    @patch('telegram_assistant.views.get_ngrok_url', return_value='https://test.ngrok.io')
    @patch('telegram_assistant.views.check_env_file', return_value=True)
    @patch('telegram_assistant.views.get_telegram_token', return_value='123456789:ABCdefGHIjklMNOpqrSTUvwxyz')
    @patch('telegram_assistant.views.mask_token', return_value='123456*:ABCD****xyz')
    @patch('telegram_assistant.views.validate_telegram_token', return_value=(True, 'testbot'))
    def test_check_status_json(self, mock_valid, mock_mask, mock_token, mock_env, mock_url, mock_ngrok):
        response = self.client.get(reverse('telegram_assistant:check_status'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['running'])
        self.assertEqual(data['url'], 'https://test.ngrok.io')
        self.assertTrue(data['env_exists'])
        self.assertTrue(data['token_exists'])
        self.assertTrue(data['token_valid'])
        self.assertEqual(data['token_message'], 'testbot')
