# hanabi-live-bot

A bot for playing Hanabi on [hanabi.live](https://hanabi.live/)
It follows H-Convention, currently at really dumb level.

<br>

## Setup Instructions

- Clone the repository:
  - `git clone git@github.com:NicolleLouis/hanabi-bot.git`
  - `cd hanabi-bot`
- Install the dependencies:
  - `poetry install`
- Set up environment variables:
  - `cp .env_template .env`
  - `vim .env`
- Run it:
  - `make single` to run a single bot
  - `make multi` to run 4 bots at once
  - You can easily customize the number of bots by changing the `-number` variable in the Makefile
- In a browser, log on to the website and start a new table.
- In the pre-game chat window, send a private message to the bot:
  - `/msg [username] /join`
- Then, start the game and play!
