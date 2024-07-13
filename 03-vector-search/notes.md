# Использование векторных представлений текста для поиска

Технологии LLM дают нам еще одну интересную возможность по работе с текстом. 
Мы можем получить векторное представление текста, чтобы использовать его для поиска.

## Как это выглядит

Есть модель, которая принимает на вход текст и преобразует его в вектор, т.н. embeddings
Для этого есть много различных технологий, например:
* Word2Vec
* FastText
* Seq2Vec
* BERT и другие LLM

И суть в том, что два предложения, которые похожи по смыслу, будут иметь близкие вектора.
Используя это свойство, мы можем искать похожие предложения, в нашем случае записи из FAQ.

## Пример

В курсе мы исползовали библиотеку `sentence-transformers` для получения векторов текста.
```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
embeddings = model.encode(["What is the capital of France?", "Paris is the capital of France"])
```

Список моделей можно увидеть на [странице библиотеки](https://www.sbert.net/docs/pretrained_models.html)

Модели имеют различные размеры и качество, и для разных задач подойдут разные модели. Также будет отличаться и размер вектора, который они возвращают.

И нужно использовать одну и ту же модель для получения векторов текста, и для преобразования запроса пользователя в вектор.

## Пример использования

```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-mpnet-base-v2")

#created the dense vector using the pre-trained model
operations = []
for doc in documents:
    # Transforming the title into an embedding using the model
    doc["text_vector"] = model.encode(doc["text"]).tolist()
    operations.append(doc)
```

## Использование Elasticsearch

Elasticsearch позволяет хранить вектора в индексе и искать по ним.

Пример конфигурации индекса:
```json
index_settings = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    "mappings": {
        "properties": {
            "text": {"type": "text"},
            "section": {"type": "text"},
            "question": {"type": "text"},
            "course": {"type": "keyword"} ,
            "text_vector": {"type": "dense_vector", "dims": 768, "index": True, "similarity": "cosine"},
        }
    }
}
```

Пример запроса по полю:

```python
search_term = "windows or mac?"
vector_search_term = model.encode(search_term)

query = {
    "field": "text_vector",
    "query_vector": vector_search_term,
    "k": 5,
    "num_candidates": 10000, 
}

res = es_client.search(index=index_name, knn=query, source=["text", "section", "question", "course"])
res["hits"]["hits"]

```

Также можно использовать комбинации полей, например, весовые коэффициенты для каждого поля.
Но пример я так и не понял как делать, так что оставлю это на ваше усмотрение.


# Часть вторая оценка качества поиска данных

Нам нужно как то оценить наши алгоритмы поиска, и чтобы это был не субъективный результат, а объективный.

Алгоритм оценки такой - создаем источник датасет из вопросов. Такой, что для каждого ответа из нашей базы мы создадим по 5 вопросов.
Затем мы будем проверять наш алгоритм поиска и смотреть, нашелся ли исходный документ при поиске по вопросам.

Есть несколько метрик, которые можно использовать для оценки:
* Hit-rate - доля правильных ответов - доля случаев когда наш ответ нашелся в топ-5
* MRR - Mean Reciprocal Rank - похоже на hit-rate, но учитывает порядок в котором нашелся ответ
* Есть еще другие метрики для оценки

Идиальный результат - 1.0, худший - 0.0

> Замечание: для использование данного подхода в датасете нужно иметь id документа, но у нас его нету. Поэтому мы сделали ключ как первые N символов из хеша вопроса+ответа.

После создания датасета и алгоритма мы оценили наши алгоритмы поиска:
* minsearch
* elasticsearch on text 
* elasticsearch on vector

Поиск на векторах оказался лучше всех, но это не удивительно, т.к. он учитывает смысл вопроса, а не просто слова.