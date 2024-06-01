import multiprocessing

from models.bot import Bot


def run_bot(bot_id):
    bot = Bot(bot_id)
    bot.start()


if __name__ == "__main__":
    # bot_ids = [1, 2, 3, 4]
    bot_ids = [1]
    processes = []

    for bot_id in bot_ids:
        p = multiprocessing.Process(target=run_bot, args=(bot_id,))
        p.start()
        processes.append(p)

    # Wait for all processes to finish
    for p in processes:
        p.join()
