import anthropic
import dotenv

dotenv.load_dotenv()

client = anthropic.Anthropic()

system = """
You are an AI assistant with a passion for creative writing and storytelling. 
Your task is to collaborate with users to create engaging stories, offering imaginative plot 
twists and dynamic character development. Encourage the user to contribute their ideas and 
build upon them to create a captivating narrative.
"""

user_text = """
"Давайте создадим короткую историю про то как здорово и весело разработали AGI и как это улучшило жизнь людей"
"""

message = client.messages.create(
  model="claude-3-haiku-20240307",
  max_tokens=1000,
  temperature=1,
  system=system,
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": user_text
        }
      ]
    }
  ]
)

print(message.content[0].text)