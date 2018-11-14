Example configuration

```json5
{
  "allow_retweets": false,
  "locations": [],
  "track": ["\"weather\" :("],
  "null_delimit": true
}
```

Null delimit will delimit the stream output with null-bytes (in case having a delimiter for the JSON responses is useful to you).
