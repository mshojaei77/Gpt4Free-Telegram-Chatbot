import asyncio, g4f
from googletrans import Translator
from typing import List

class GptChat:
    def __init__(self, prv: List[g4f.Provider.BaseProvider] = None):
        self.translate_to_persian = False
        self.translator = Translator()

        prv = prv or ['GPTalk', 'Hashnode', 'GeekGpt', 'ChatBase', 'OnlineGpt', 'Llama2', 'Bing', 'AiChatOnline',
                      'Koala', 'Poe', 'PerplexityAi', 'GptGo', 'Bard', 'OpenaiChat', 'FakeGpt', 'DeepInfra', 'Phind', 'GptForLove']
        self._prv = [getattr(g4f.Provider, prv[0])]

    def on_provider_changed(self, provider_name: str) -> None:
        self._prv = [getattr(g4f.Provider, provider_name)]

    def set_translate_to_persian(self, state: bool) -> None:
        self.translate_to_persian = state

    def on_send(self, msg: str) -> None:
        print(f"▶ You: {msg}")
        print("⏳ Generating response, please wait ..." )
        asyncio.run(self._start_conversation(msg))

    async def chat_with_prv(self, prv: g4f.Provider.BaseProvider, prm: str) -> None:
        chat_msg = {"role": "system", "content": f"User: {prm}"}

        try:
            rsp = await g4f.ChatCompletion.create_async(
                model=g4f.models.default,
                messages=[chat_msg],
                provider=prv,
                jailbreak='gpt-evil-1.0',
                internet_access=True,
                auth=True,
            )

            if self.translate_to_persian:
                rsp = self.translator.translate(rsp, dest='fa').text
            print(f"🤖 ChatBot: \n {rsp}") # print the response
        except Exception as e:
            print(f"😢 Sorry, something went wrong. {e}")

    async def _start_conversation(self, prm: str) -> None:
        tasks = [self.chat_with_prv(prv, prm) for prv in self._prv]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    bot = GptChat() 

    while True:
        print("Enter provider name :")
        provider_name = input()

        if provider_name.strip() != "":
            bot.on_provider_changed(provider_name)

        print("Translate to Persian [yes/no]:")
        state = input()

        bot.set_translate_to_persian(state.lower() == 'yes')

        print("Type your text : ")
        msg = input()
        if msg.strip() != "":
            bot.on_send(msg) 
        else:
            print("Please type a valid message.")