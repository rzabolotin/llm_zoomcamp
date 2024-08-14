# Q1. Running Mage

Now mage is running on http://localhost:6789/

What's the version of mage?

**Answer**: v0.9.72

# Q2. Reading the documents

Copy the code to the editor How many FAQ documents we processed?

```python
    faq_documents = {
    'llm-zoomcamp': '1m2KexowAXTmexfC5rVTCSnaShvdUQ8Ag2IEiwBDHxN0',
}

documents = []

for course, file_id in faq_documents.items():
    print(course)
    course_documents = read_faq(file_id)
    documents.append({'course': course, 'documents': course_documents})

return {"documents": documents}
```

**Answer**: 1

# Q3. Chunking

How many documents (chunks) do we have in the output?

* 66
* 76
* **86**
* 96

# Q4. Export

Now execute the block.

What's the last document id?

Also note the index name.
**Answer:**
last document: 6fc3236a
index_name: documents_20240813_1009

# Q5. Testing the retrieval

```python

from typing import Dict, List

from elasticsearch import Elasticsearch

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def search(*args, **kwargs) -> List[Dict]:
    connection_string = kwargs.get('connection_string', 'http://localhost:9200')
    index_name = kwargs.get('index_name', 'documents')
    top_k = kwargs.get('top_k', 5)

    # Hardcoded query
    query = "When is the next cohort?"

    es_client = Elasticsearch(connection_string)

    response = es_client.search(
        index=index_name,
        body={
            "size": top_k,
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["text", "section", "question"]
                }
            }
        }
    )

    print(response['hits']['hits'][0])

    return [hit['_source'] for hit in response['hits']['hits']]


@test
def test_output(output, *args) -> None:
    assert output is not None, 'The output is undefined'
    assert isinstance(output, list), 'The output should be a list'
    assert len(output) > 0, 'The output list should not be empty'
    for item in output:
        assert isinstance(item, dict), 'Each item in the output should be a dictionary'

```

Let's use the following query: "When is the next cohort?"

What's the ID of the top matching result?

```json
{
  '_index': 'documents_20240813_1009',
  '_id': '4cI3S5EBmo3lK9SDcC0X',
  '_score': 8.443945,
  '_source': {
    'text': 'Summer 2025 (via Alexey).',
    'section': 'General course-related questions',
    'question': 'When will the course be offered next?',
    'course': 'llm-zoomcamp',
    'document_id': 'bf024675'
  }
}
```
**Answer:** bf024675



# Q6. Reindexing

The ID of this document is 1T3MdwUvqCL3jrh3d3VCXQ8xE0UqRzI3bfgpfBq3ZWG0.

Let's re-execute the entire pipeline with the updated data.

For the same query "When is the next cohort?". What's the ID of the top matching result?

{'_index': 'documents_20240814_3128', '_id': 'zFonT5EBq3Uve6oiuacp', '_score': 17.212463, '_source': {'text': 'Summer 2026.', 'section': 'General course-related questions', 'question': 'When is the next cohort?', 'course': 'llm-zoomcamp', 'document_id': 'b6fa77f3'}}

**Answer:** b6fa77f3
