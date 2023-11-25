import g4f
import asyncio
from aiohttp import ClientResponseError
import time
from concurrent.futures import ThreadPoolExecutor

prompt = input("Prompt: ")
timeout = int(input("Timeout: "))

_providers = list(set([
    g4f.Provider.AItianhu,
    g4f.Provider.AItianhuSpace,
    g4f.Provider.Acytoo,
    g4f.Provider.AiAsk,
    g4f.Provider.AiChatOnline,
    g4f.Provider.AiService,
    g4f.Provider.Aibn,
    g4f.Provider.Aichat,
    g4f.Provider.Ails,
    g4f.Provider.Aivvm,
    g4f.Provider.AsyncGeneratorProvider,
    g4f.Provider.AsyncProvider,
    g4f.Provider.Bard,
    g4f.Provider.BaseProvider,
    g4f.Provider.Berlin,
    g4f.Provider.Bing,
    g4f.Provider.ChatAiGpt,
    g4f.Provider.ChatAnywhere,
    g4f.Provider.ChatBase,
    g4f.Provider.ChatForAi,
    g4f.Provider.Chatgpt4Online,
    g4f.Provider.ChatgptAi,
    g4f.Provider.ChatgptDemo,
    g4f.Provider.ChatgptDemoAi,
    g4f.Provider.ChatgptDuo,
    g4f.Provider.ChatgptFree,
    g4f.Provider.ChatgptLogin,
    g4f.Provider.ChatgptNext,
    g4f.Provider.ChatgptX,
    g4f.Provider.CodeLinkAva,
    g4f.Provider.Cromicle,
    g4f.Provider.DeepInfra,
    g4f.Provider.DfeHub,
    g4f.Provider.EasyChat,
    g4f.Provider.Equing,
    g4f.Provider.FakeGpt,
    g4f.Provider.FastGpt,
    g4f.Provider.Forefront,
    g4f.Provider.FreeGpt,
    g4f.Provider.GPTalk,
    g4f.Provider.GeekGpt,
    g4f.Provider.GetGpt,
    g4f.Provider.GptChatly,
    g4f.Provider.GptForLove,
    g4f.Provider.GptGo,
    g4f.Provider.GptGod,
    g4f.Provider.H2o,
    g4f.Provider.Hashnode,
    g4f.Provider.HuggingChat,
    g4f.Provider.Koala,
    g4f.Provider.Komo,
    g4f.Provider.Liaobots,
    g4f.Provider.Llama2,
    g4f.Provider.Lockchat,
    g4f.Provider.MikuChat,
    g4f.Provider.MyShell,
    g4f.Provider.Myshell,
    g4f.Provider.NoowAi,
    g4f.Provider.OnlineGpt,
    g4f.Provider.Opchatgpts,
    g4f.Provider.OpenAssistant,
    g4f.Provider.OpenaiChat,
    g4f.Provider.PerplexityAi,
    g4f.Provider.Phind,
    g4f.Provider.Poe,
    g4f.Provider.ProviderUtils,
    g4f.Provider.Raycast,
    g4f.Provider.RetryProvider,
    g4f.Provider.TalkAi,
    g4f.Provider.Theb,
    g4f.Provider.ThebApi,
    g4f.Provider.V50,
    g4f.Provider.Vercel,
    g4f.Provider.Vitalentum,
    g4f.Provider.Wewordle,
    g4f.Provider.Wuguokai,
    g4f.Provider.Ylokh,
    g4f.Provider.You,
    g4f.Provider.Yqcloud
]))

response_times = {}

def run_provider(provider: g4f.Provider.BaseProvider):
    start_time = time.time()
    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.default,
            messages=[{"role": "user", "content": prompt }],
            provider=provider,
            auth=True,
        )
        end_time = time.time()
        print("\n -------------------- \n",f" ✅ {provider.__name__}:", response)
        print("Response time (seconds):", end_time - start_time)

        response_times[provider.__name__] = end_time - start_time
    except Exception as e:
        print(f" ❌ {provider.__name__}:", e)

def run_all():
    with ThreadPoolExecutor() as executor:
        executor.map(run_provider, _providers)

    sorted_response_times = sorted(response_times.items(), key=lambda x: x[1])  # Sort the dictionary by the response time
    print("\n ----------------- \n")
    print("Ranking of the providers by the response time:")  # Print the ranking of the providers by the response time
    for i, (provider, time) in enumerate(sorted_response_times, start=1):
        print(f"{i}. {provider}: {time} seconds")

run_all()