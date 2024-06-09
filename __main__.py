import argparse
import multiprocessing

from models.bot import Bot


def run_bot(bot_id):
    bot = Bot(bot_id)
    bot.start()


def multi_bot(bot_ids):
    processes = []

    for bot_id in bot_ids:
        p = multiprocessing.Process(target=run_bot, args=(bot_id,))
        p.start()
        processes.append(p)

    # Wait for all processes to finish
    for p in processes:
        p.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-bot', type=int, help='Bot to use')
    parser.add_argument('-multi', type=bool, help='Should use multiple bots')
    parser.add_argument('-number', type=int, help='Number of bots')

    args = parser.parse_args()

    if args.multi:
        multi_bot(range(1, args.number + 1))
    else:
        run_bot(args.bot)
