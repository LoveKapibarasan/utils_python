from openai import OpenAI
from get_api_key import get_api_key

api_key = get_api_key()
client = OpenAI(api_key=api_key)

while True:
    user_input = input("You: ")

    result = client.responses.create(
        model="gpt-5",
        input=user_input,
        reasoning={ "effort": "low" },
        text={ "verbosity": "low" },
    )
    print("ChatGPT:", result.output_text)
    with open("chat_log.txt", "a") as log_file:
        log_file.write(f"You: {user_input}\n")
        log_file.write(f"ChatGPT: {result.output_text}\n")
        log_file.write("\n\n")

"""
https://platform.openai.com/docs/guides/latest-model
| パラメータ                     | 役割                                     |
| ------------------------- | -------------------------------------- |
| `reasoning.effort`        | 推論トークン量（minimal / low / medium / high） |
| `text.verbosity`          | 出力トークン量（low / medium / high）           |
| `tools` / `allowed_tools` | カスタムツール呼び出し制約                          |
| *preambles*               | ツール呼び出し前に“なぜ使うか”を自動説明                  |

"""