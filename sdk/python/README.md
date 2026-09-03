# Python SDK

A small server-side SDK that demonstrates how an application could evaluate flags through the platform API.

This SDK intentionally contains:

- configuration object
- reusable HTTP transport
- typed evaluation context
- error types
- retries
- short local cache
- example usage
- tests

In a mature system the SDK might instead receive a streamed or polled copy of flag configuration and evaluate locally. V1 uses remote evaluation because it keeps the architecture easy to trace.
