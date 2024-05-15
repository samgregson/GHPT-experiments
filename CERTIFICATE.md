### Introduction
This file explains how to make sure that `LangSmith` is allowed to access `api.smith.langchain.com`.
Following these steps will prevent the following error message:

`Failed to batch ingest runs: LangSmithConnectionError('Connection error caused failure to POST https://api.smith.langchain.com/runs/batch  in LangSmith API. Please confirm your internet connection.. SSLError(MaxRetryError("HTTPSConnectionPool(host=\'api.smith.langchain.com\', port=443): Max retries exceeded with url: /runs/batch (Caused by SSLError(SSLCertVerificationError(1, \'[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1000)\')))"))')`

Background: `certifi` is a Python package that provides a collection of Root Certificates. It's used by `requests` and many other packages to trust the standard set of public CAs. We want to add custom certificates (a corporate certificate). We export new "bundle" that from the corporate certificate and use that.

### Export Certificate
Export certificates to a file on your machine, follow the first part of this article: https://learn.microsoft.com/en-us/azure/application-gateway/mutual-authentication-certificate-management

### Add Certifacatet to VS Code environment
In your .env folder create a new variable: REQUESTS_CA_BUNDLE=the\location\of\your\file.cer

You will note that the python code contains the following to ensure that these certificates are used (not sure whether this is required):
```py
import os
import ssl
context = ssl.create_default_context(cafile=os.environ.get("REQUESTS_CA_BUNDLE"))
```

### Verify Certifacate Has Been Added Correctly
To verify that this has worked you can test it by running the foloowing:

```py
import requests
requests.get("https://api.smith.langchain.com/docs")
```

expected response:
`<Response [200]>`
