from deepgram import DeepgramClient

from app.config import DEEPGRAM_API_KEY

deepgram = DeepgramClient(DEEPGRAM_API_KEY)


async def create_deepgram_connection():

    dg_connection = deepgram.listen.websocket.v("1")

    return dg_connection