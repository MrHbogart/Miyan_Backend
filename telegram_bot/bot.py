import os
import json
import time
import requests
from pathlib import Path

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext


API_URL = os.getenv('API_URL', 'http://web:8000').rstrip('/')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
SHARED_SECRET = os.getenv('TELEGRAM_SHARED_SECRET') or os.getenv('BOT_SHARED_SECRET')
BOT_STATE_PATH = os.getenv('BOT_STATE_PATH', '/data/state.json')
STATE_FILE = Path(BOT_STATE_PATH)


def load_state():
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except Exception:
            return {}
    return {}


def save_state(state):
    # ensure parent directory exists
    try:
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass
    STATE_FILE.write_text(json.dumps(state))


state = load_state()


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hello — this bot lets staff link their account and submit nightly inventory.\n"
        "Use /link <your-bot-token> to link your Telegram account, then /record to submit a record.\n"
        "Example: /record 1 2 15 Optional note"
    )


def link(update: Update, context: CallbackContext):
    args = context.args
    if not args:
        update.message.reply_text('Usage: /link <bot_token>')
        return

    bot_token = args[0].strip()
    telegram_id = str(update.effective_user.id)
    payload = {'bot_token': bot_token, 'telegram_id': telegram_id}
    try:
        r = requests.post(f'{API_URL}/api/inventory/staff/link/', json=payload, timeout=10)
    except Exception as e:
        update.message.reply_text(f'Error connecting to server: {e}')
        return

    if r.status_code != 200:
        update.message.reply_text(f'Link failed: {r.text}')
        return

    data = r.json()
    username = data.get('username')

    # Request token using secure endpoint and shared secret
    headers = {'X-BOT-SECRET': SHARED_SECRET} if SHARED_SECRET else {}
    try:
        r2 = requests.post(
            f'{API_URL}/api/inventory/get-token/', json={'telegram_id': telegram_id}, headers=headers, timeout=10
        )
    except Exception as e:
        update.message.reply_text(f'Linked as {username}, but failed to fetch token: {e}')
        return

    if r2.status_code == 200:
        token = r2.json().get('token')
        if token:
            state[telegram_id] = {'token': token, 'username': username}
            save_state(state)
            update.message.reply_text(f'Linked as {username}. You can now use /record to submit inventory.')
            return

    # Fallback: if server returned token on initial link, keep it
    token = data.get('token')
    if token:
        state[telegram_id] = {'token': token, 'username': username}
        save_state(state)
        update.message.reply_text(f'Linked as {username}. You can now use /record to submit inventory.')
        return

    update.message.reply_text('Linked but no token available.')


def record(update: Update, context: CallbackContext):
    args = context.args
    telegram_id = str(update.effective_user.id)
    if telegram_id not in state:
        # try to fetch token dynamically if shared secret is configured
        if SHARED_SECRET:
            headers = {'X-BOT-SECRET': SHARED_SECRET}
            try:
                rtk = requests.post(f'{API_URL}/api/inventory/get-token/', json={'telegram_id': telegram_id}, headers=headers, timeout=10)
                if rtk.status_code == 200:
                    tok = rtk.json().get('token')
                    state[telegram_id] = {'token': tok}
                    save_state(state)
                else:
                    update.message.reply_text('You are not linked. Use /link <bot_token> first.')
                    return
            except Exception:
                update.message.reply_text('You are not linked. Use /link <bot_token> first.')
                return
        else:
            update.message.reply_text('You are not linked. Use /link <bot_token> first.')
            return

    if len(args) < 3:
        update.message.reply_text('Usage: /record <branch_id> <item_id> <quantity> [note]')
        return

    branch_id = args[0]
    item_id = args[1]
    quantity = args[2]
    note = ' '.join(args[3:]) if len(args) > 3 else ''

    try:
        qty = int(quantity)
    except ValueError:
        update.message.reply_text('Quantity must be an integer.')
        return

    token = state[telegram_id]['token']
    headers = {'Authorization': f'Token {token}'}
    payload = {'branch': branch_id, 'item': item_id, 'quantity': qty, 'note': note}
    try:
        r = requests.post(f'{API_URL}/api/inventory/records/', json=payload, headers=headers, timeout=10)
    except Exception as e:
        update.message.reply_text(f'Error connecting to server: {e}')
        return

    if r.status_code in (200, 201):
        update.message.reply_text('Record submitted successfully.')
    else:
        try:
            text = r.json()
        except Exception:
            text = r.text
        update.message.reply_text(f'Failed to submit: {text}')


def main():
    if not TELEGRAM_TOKEN:
        print('TELEGRAM_TOKEN env var is required')
        return

    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('link', link, pass_args=True))
    dp.add_handler(CommandHandler('record', record, pass_args=True))

    # list branches and items
    def branches_cmd(update: Update, context: CallbackContext):
        try:
            r = requests.get(f'{API_URL}/api/inventory/branches/', timeout=10)
            if r.status_code == 200:
                items = r.json()
                lines = [f"{b['id']}: {b['name']}" for b in items]
                update.message.reply_text('Branches:\n' + '\n'.join(lines[:50]))
            else:
                update.message.reply_text('Failed to fetch branches')
        except Exception as e:
            update.message.reply_text(f'Error: {e}')

    def items_cmd(update: Update, context: CallbackContext):
        try:
            r = requests.get(f'{API_URL}/api/inventory/items/', timeout=10)
            if r.status_code == 200:
                items = r.json()
                lines = [f"{it['id']}: {it['name']} ({it.get('unit','')})" for it in items]
                update.message.reply_text('Items:\n' + '\n'.join(lines[:100]))
            else:
                update.message.reply_text('Failed to fetch items')
        except Exception as e:
            update.message.reply_text(f'Error: {e}')

    dp.add_handler(CommandHandler('branches', branches_cmd))
    dp.add_handler(CommandHandler('items', items_cmd))

    print('Starting bot...')
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
