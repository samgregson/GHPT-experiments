### Introduction
This file explains how to make sure that `LangSmith` is allowed to access `api.smith.langchain.com`.
Following these steps will prevent the following error message:

`Failed to batch ingest runs: LangSmithConnectionError('Connection error caused failure to POST https://api.smith.langchain.com/runs/batch  in LangSmith API. Please confirm your internet connection.. SSLError(MaxRetryError("HTTPSConnectionPool(host=\'api.smith.langchain.com\', port=443): Max retries exceeded with url: /runs/batch (Caused by SSLError(SSLCertVerificationError(1, \'[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1000)\')))"))')`

### Get Certificate
To get an SSL certificate from a website using Google Chrome, follow these steps:

1. Navigate to the website from which you want to get the certificate (`api.smith.langchain.com`).
2. Click on the site information icon to the left of the URL.

  ![image](https://github.com/samgregson/GHPT-experiments/assets/12054742/d96f6851-f0b9-416c-8521-e484819a80f8)
   
3. Click on `Connection is Secure`
4. Click on `Certificate is valid` in the dropdown.
5. In the Certificate viewer that opens, go to the `Details` tab.
6. Click on `Export...` to start the certificate export wizard.
7. Save somewhere on your computer with the extension `.pem`.

The certificate will be saved in the location you specified. You can then use this certificate file in your Python scripts or other applications.

### Add Certifacatet to VS Code environment

`certifi` is a Python package that provides a collection of Root Certificates. It's used by `requests` and many other packages to trust the standard set of public CAs. If you want to add a custom certificate (like a self-signed certificate or a corporate certificate) to the bundle that `certifi` provides, you can't directly add it to `certifi`'s bundle. However, you can create a new bundle that includes both `certifi`'s bundle and your custom certificate.

Here's how you can do it:

1. Get the path to `certifi`'s bundle:
   
   ```py
   import certifi

   print(certifi.where())
   ```
   This will print the path to the file that includes certifi's bundle.

2. Concatenate your certificate with `certifi`'s bundle:

3. Replace /path/to/your/certificate.pem with the path to your certificate file and /path/to/certifi/cacert.pem with the path printed by the previous Python script.

   ```py
   import ssl
   import certifi

   context = ssl.create_default_context(cafile=certifi.where())
   ```

5. Now, when you create an SSL context, you can use the updated `certifi` bundle:

Please note that this will modify `certifi`'s bundle, which may affect other scripts and applications that use `certifi`. If you want to avoid this, you can copy `certifi`'s bundle to a new file, add your certificate to the new file, and use the new file as the cafile parameter in `ssl.create_default_context()`.

### Verify Certifacate Has Been Added Correctly
To verify if a certificate is trusted by your system, you can use the OpenSSL command-line tool. Here's how you can do it:

1. Open your terminal.
2. Run the following command:
   
```py
openssl verify -CAfile /path/to/your/cacert.pem /path/to/your/certificate.pem
```
Replace `/path/to/your/cacert.pem` with the path to your CA bundle file and `/path/to/your/certificate.pem` with the path to the certificate you want to verify.

This command will check if the certificate is signed by a trusted CA included in the CA bundle file. If the certificate is trusted, it will print `OK`. If it's not trusted, it will print an error message.

Please note that the CA bundle file should include the root certificates of all the CAs you trust. On a Unix-like system, this file is usually located at `/etc/ssl/certs/ca-certificates.crt`. On a Windows system, the trusted certificates are stored in the Windows Certificate Store, and you need to use Windows tools to manage them.
