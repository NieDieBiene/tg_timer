import ptbot
import os

from pathlib import Path
from dotenv import load_dotenv
from pytimeparse import parse


dotenv_path = Path('.env')
load_dotenv(dotenv_path)
TG_TOKEN = os.getenv('TG_TOKEN')
TG_CHAT_ID = os.getenv('TG_CHAT_ID')
bot = ptbot.Bot(TG_TOKEN)


def reply(chat_id, text):
    time = parse(text)
    message_id = bot.send_message(chat_id, "Осталось {} секунд!".format(time))
    bot.create_countdown(
        time,
        notify_progress,
        chat_id=chat_id,
        message_id=message_id,
        total_time=time
    )
    bot.create_timer(time, notify, chat_id=chat_id)


def notify(chat_id):
    bot.send_message(chat_id, "Время вышло!")


def notify_progress(secs_left, chat_id, message_id, total_time):
    seconds_passed = total_time - secs_left
    progress_text = render_progressbar(
        total=total_time,
        iteration=seconds_passed
    )
    bot.update_message(
        chat_id,
        message_id,
        "Осталось {} секунд!".format(secs_left) + "\n" + progress_text
    )


def render_progressbar(
    total,
    iteration,
    prefix='',
    suffix='',
    length=30,
    fill='█',
    zfill='░'
):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def main():
    bot.reply_on_message(reply)
    bot.run_bot()


if __name__ == '__main__':
    main()
