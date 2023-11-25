import telebot
import asyncio, g4f
from telebot import types
from typing import List
from googletrans import Translator

TOKEN = "YOUR_TOKEN"
bot = telebot.TeleBot(TOKEN)
translator = Translator()

class GptChat:
    def __init__(self, prv: List[g4f.Provider.BaseProvider] = None):

        self.providers = ['GeekGpt','ChatForAi','Bing', 'Llama2', 'Hashnode' ,'GptForLove', 'OnlineGpt', 'GPTalk' , 'DeepInfra',
                          'AiChatOnline','Liaobots', 'Chatgpt4Online','ChatgptNext', 'ChatAnywhere']
        prv = prv or [self.providers[0]]
        self.current_provider = None
        self._prv = [getattr(g4f.Provider, prv[0])]

    def set_provider(self, provider_name: str) -> None:
        self.current_provider = provider_name
        self._prv = [getattr(g4f.Provider, self.current_provider)] if provider_name else self._prv

    def on_send(self, msg: types.Message) -> None:
        self.set_provider(self.providers[0]) if not self.current_provider else None
        bot.send_chat_action(msg.chat.id, 'typing')
        asyncio.run(self._start_conversation(msg))

    async def chat_with_prv(self, prv: g4f.Provider.BaseProvider, prm: str) -> str:
        chat_msg = {"role": "system", "content": f"{prm}"}

        try:
            rsp = await g4f.ChatCompletion.create_async(
                model=g4f.models.default,
                messages=[chat_msg],
                provider=prv,
                jailbreak='gpt-evil-1.0',
                internet_access=True,
                auth=True,
            )
            return f" {self.current_provider}: \n {rsp}"
        except Exception as e:
            return f"Provider is not available at the moment try another providers.\n /providers "

    async def _start_conversation(self, prm: types.Message) -> None:
        tasks = [self.chat_with_prv(prv, prm.text) for prv in self._prv]
        responses = await asyncio.gather(*tasks)
        for response in responses:
            keyboard = types.InlineKeyboardMarkup()
            persian_translate_btn = types.InlineKeyboardButton("Translate to Persian", callback_data='translate_persian')
            keyboard.add(persian_translate_btn)
            bot.reply_to(prm, response, reply_markup=keyboard)

bot_instance = GptChat()

@bot.message_handler(commands=['providers'])
def Choose_Provider(message):
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    buttons = [types.InlineKeyboardButton(provider, callback_data=provider) for provider in bot_instance.providers]
    keyboard.add(*buttons)
    bot.reply_to(message, "Select a Provider (press /more for details)", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == 'translate_persian':
            translated_text = translator.translate(call.message.text, dest='fa')
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=translated_text.text)
        else:
            provider_data = call.data
            bot_instance.set_provider(provider_data)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Selected Provider: {provider_data}")

@bot.message_handler(commands=['more'])
def more_details(message):
    bot.reply_to(message, """| AI Provider         | Model         | Response Speed |
|---------|--------|-----------|
| GeekGpt             | GPT-3.5       | Low                      |
| OnlineGpt           | GPT-4         | Low                      |
| GPTalk              | GPT-4         | Low                      |
| Hashnode            | GPT-4         | Low                      |
| ChatForAi           | GPT-3         | Low                      |
| DeepInfra           | LLaMA         | High                     |
| Llama2              | LLaMA         | High                     |
| Bing                | GPT-4         | High                     |
| AiChatOnline        | GPT-3         | Low                      |
| Liaobots            | Not specified | Not specified            |
| Chatgpt4Online      | GPT-4         | High                     |
| GptForLove          | GPT-3.5       | High                     |
| ChatgptNext         | GPT-4         | High                     |
| ChatAnywhere        | Not specified | Not specified            |""")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    if message.text.strip() != "":
        bot_instance.on_send(message)
    else:
        bot.reply_to(message, "Please type a valid message.")

bot.infinity_polling()