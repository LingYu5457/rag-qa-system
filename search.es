GET _cat/indices?v
GET _search
{
  "size": 100,
  "query": {
    "match_all": {}
  }
}