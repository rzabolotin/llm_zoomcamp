# Использование открытых LLM моделей

## Описание
Как альтернатива proprietory LLM есть открытые LLM. Это такие модели, чьи веса доступны публично, и их можно использовать на своем компьютере.
Обычно для хорошей работы таких моделей требуется видеокарта с большим количество памяти, но некоторые модели можно использовать и на CPU.

В данном разделе мы научились использованию такие модели
Первая часть требует наличия видеокарты, и мы использовали арендованный сервер и библиотеку `transformers` для загрузки модели и генерации текста.

## Hugging face

![hugging face logo](images/img.png)

[Hugging face](https://huggingface.co/) - это платформа (а заодно и библиотека для python) для работы с LLM моделями. На платформе можно делиться весами обученных моделей, и использовать их для разных задач (в том числе для генерации текста).

Мы можем запускать модель локально, если у нас есть GPU, арендовать сервер (в курсе мы использовали Saturn Cloud) или использовать платформы на подобии Google Colab. 

Для работы с моделями на huggingface можно использовать библиотеку `transformers`. Она позволяет загружать модели и использовать их. 

На hugging face есть множество доступных публично моделей. Мы попробовали работать с некоторыми "небольними" LLM, которым хватило 16 Гб видеопамяти: 
- FLAN-T5 от Google
- PHI-3 от Microsoft
- Mistral 

Для запуска кода необходимо установить библиотеки:
* transformers
* accelerate
* bitsandbytes
* sentencepiece
* torch

Мои ноутбуки, с примерами запуска моделей:
* [FLAN-T5](<02-open-llm/1. FLAT T5.ipynb>)
* [PHI-3](<02-open-llm/2. PHI 3.ipynb>)
* [Mistral](<02-open-llm/3. Mistral.ipynb>)

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