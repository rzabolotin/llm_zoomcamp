# Использование открытых LLM моделей

## Описание
В данном разделе мы научились использованию открытых LLM.
Первая часть требует наличия видеокарты, и мы использовали библиотеку `transformers` для загрузки модели и генерации текста.

## Hugging face

На сайти [huggingface](https://huggingface.co/) есть множество доступных публично моделей. Мы попробовали работать с 
- FLAN-T5 от Facebook
- PHI-3 от Microsoft
- Mistral 

Для запуска кода необходимо установить библиотеки:
* transformers
* accelerate
* bitsandbytes
* sentencepiece
* torch

Мои ноутбуки:
* [FLAN-T5](1. FLAT T5.ipynb)
* [PHI-3](2. PHI 3.ipynb)
* [Mistral](3. Mistral.ipynb)

### Важные замечания
* Для указания папки в которой хранить модели нужно указать переменную окружения
```python
os.environ['HF_HOME'] = '/run/cache/'
```
* Для некоторых моделей на huggingface необходимо принять соглашение, и потом для получения самой модели нужно залогиниться в api. Например для Mistral

## Использование ollama

Ollama это проект, который позволяет запукать LLM на своем компьютере, работает не очень, но можно что-то тестировать.
Можно установить ее через wsl:

```bash
curl -fsSL https://ollama.com/install.sh | sh

ollama start
ollama serve phi3
```

Вести диалог можно в виде чата `ollama run phi3` или в виде вызова api. Можно использовать библиотеку openai

```python
from openai import OpenAI

client = OpenAI(
    base_url='http://localhost:11434/v1/',
    api_key='ollama',
)

```

Также ollama можно использовать в docker контейнере. 

Вот пример приложения которое мы сделали локально:
* [docker-compose](docker-compose.yaml)
* [ноутбук](4.run-ollama-local.ipynb)
* [streamlit приложение для чата](qa_faq.py)


## Выводы

Технологии LLM это не только закрытые API, но и открытые модели, которые можно использовать на своем компьютере.

И конечно они намного хуже закрытых, но тоже технологии продвигаются вперед, и открытые модели также становятся лучше.

## Ссылки

* [huggingface](https://huggingface.co/)
* [ollama](https://ollama.com/)
* [saturn cloud](https://saturncloud.io/)
* [лидерборд open llm](https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard)
* [лидерборд open llm perf](https://huggingface.co/spaces/optimum/llm-perf-leaderboard)
* [llm tutorial from huggingface](https://huggingface.co/docs/transformers/en/llm_tutorial)