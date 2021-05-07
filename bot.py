import getopt
import sys
import re
from telethon.errors import SessionPasswordNeededError
from telethon import TelegramClient, events, sync
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (
    PeerChannel
)


def startListener(opts):

    api_id = int(opts[0].__getitem__(1))
    api_hash = opts[1].__getitem__(1)
    source_username = opts[2].__getitem__(1)
    target_username = opts[3].__getitem__(1)

    shortURLRegex = r"https?:\/\/(([^\s]*)\.)?amzn\.to\/([0-9A-Za-z]+)"

    user_input_channel = source_username

    client = TelegramClient('session_name', api_id, api_hash)
    client.start()

    @client.on(events.NewMessage(chats=user_input_channel))
    async def newMessageListener(event):
        messageFromEvent = event.message.message
        print("Received event with message:\n" + messageFromEvent)
        filteredMessage = re.findall(
            shortURLRegex, messageFromEvent, flags=re.IGNORECASE)
        if (len(filteredMessage) != 0) or ('Vaccine' in messageFromEvent):
            await client.send_message(target_username, messageFromEvent)

    with client:
        client.run_until_disconnected()


argv = sys.argv[1:]
usage = "usage: bot.py --api_id=<api_id> --api_hash=<api_hash> --source_username=<source_username> --target_username=<target_username>"
try:

    opts, args = getopt.getopt(
        argv, 'a:b:c:d:', ['api_id=', 'api_hash=', 'source_username=', 'target_username='])
    # Check if the options' length is 4 (can be enhanced)
    if len(opts) == 0 or len(opts) > 4:
        print(usage)
    else:
        # Start the listener
        print("Starting the listener")
        startListener(opts)

except getopt.GetoptError:
    print(usage)
    sys.exit(1)
