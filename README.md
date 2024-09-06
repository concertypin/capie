# Capie : CRL Automately Publishing Intergretion Endpoint

**Capie** is a tool that automatically creates Certificate Revocation Lists (CRLs) with Github Action!

## Description

Capie simplifies the process of generating CRLs by automating certificate management. With just a few configurations, you can manage your CRLs efficiently and reliably.

## Installation
- Generate new repository with this template.
- Fill some information masked with `[???_HERE]` on `.github/workflows/generate.yml`.
- To make sure Github Action have read/write permissions, check `Read and write permissions` on `Settings -> Actions -> General -> Workflow permissions`.
- Link your domain with Github Pages on `Settings -> Pages -> Custom domain` and `CNAME` file. DO NOT CHECK `Enforce HTTPS`!
## Usage

1. Fill in the required configurations in the `data` directory.
    - To generate and publish CRL: 
        - See `data/example`.
        - You can place your revoked certificate on not `data/[CRL_NAME]` but `data/[CRL_NAME]/*`.
        - Allowed extension is `pem`, `crt`, `cer`, `ca`. Every certificate should be PEM formatted.
        - Place your CA certificate and private key to sign with. It's name should be same as config written at `data/[CRL_NAME]/config.yml`.
        - Private key should not be encrypted to be read by Github Action.
    - To publish CRL which is already generated:
        - Place DER-formatted CRL file on `data/[CRL_NAME]/as_is.crl`.
2. Run Github Action workflows via waiting for cron schedule or via workflow_dispatch.
3. CRLs will be published at `your-domain.com/[CRL_NAME].crl`.

## Contributing
If you'd like to contribute to Capie, feel free to fork the repository, make your changes, and submit a pull request. We welcome your PRs!

## License

This project is licensed under the MIT License.
<details>
  <summary>Full text of license here:</summary>
<pre>
Copyright 2024 concertypin

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
</pre>
</details>
