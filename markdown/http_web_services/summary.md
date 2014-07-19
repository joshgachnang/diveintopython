

11.10. Summary
--------------

The `openanything.py` and its functions should now make perfect sense.

There are 5 important features of HTTP web services that every client
should support:

-   Identifying your application [by setting a proper
    `User-Agent`](user_agent.html "11.5. Setting the User-Agent").
-   Handling [permanent redirects
    properly](redirects.html "11.7. Handling redirects").
-   Supporting [`Last-Modified` date
    checking](etags.html "11.6. Handling Last-Modified and ETag") to
    avoid re-downloading data that hasn't changed.
-   Supporting [`ETag`
    hashes](etags.html#oa.etags.example "Example 11.9. Supporting ETag/If-None-Match")
    to avoid re-downloading data that hasn't changed.
-   Supporting [gzip
    compression](gzip_compression.html "11.8. Handling compressed data")
    to reduce bandwidth even when data *has* changed.

  

