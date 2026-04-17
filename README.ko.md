# Capie : CRL 자동 게시 통합 엔드포인트

**Capie**는 GitHub Actions를 이용해 인증서 폐지 목록(CRL)을 자동으로 생성하고 게시하는 도구입니다.

## 설명

Capie는 CRL 생성 워크플로우를 자동화하여 인증서 관리를 단순화합니다. 몇 가지 설정만으로 CRL을 효율적이고 신뢰성 있게 관리하고 게시할 수 있습니다.

## 설치
- 이 템플릿으로 새 리포지토리를 생성하세요.
- `.github/workflows/generate.yml`에 표시된 `[???_HERE]` 항목들을 채우세요.
- GitHub Action이 읽기/쓰기 권한을 가지도록 `Settings -> Actions -> General -> Workflow permissions`에서 `Read and write permissions`를 확인하세요.
- 도메인을 `Settings -> Pages -> Custom domain`과 `CNAME` 파일로 연결하세요. `Enforce HTTPS`는 체크하지 마세요!

## 사용법

1. `data` 디렉터리에 필요한 설정을 채우세요.
   - 예시는 `data/example`을 참조하세요.
   - 폐지할 인증서는 `data/[CRL_NAME]/*` 아래에 넣으면 됩니다.
   - 허용 확장자는 `pem`, `crt`, `cer`, `ca` 입니다. 모든 인증서는 PEM 형식이어야 합니다.
   - 서명에 사용할 CA 인증서와 개인키를 넣으세요. 파일명은 `data/[CRL_NAME]/config.yml`에 적힌 이름과 동일해야 합니다.
   - 개인키는 리포지토리 KEK로 암호화하여 저장하고 CI에서 복호화하도록 구성하세요. GitHub Secrets에 `CA_KEK`(base64 인코딩된 32바이트 권장)를 설정하면 됩니다. 기존 키는 제공된 `scripts/migrate_encrypt.py`를 사용하여 암호화할 수 있습니다. 워크플로우는 평문 개인키가 리포지토리에 존재할 경우 경고를 표시합니다.
   - 이미 생성된 CRL을 게시하려면 DER 형식의 CRL 파일을 `data/[CRL_NAME]/as_is.crl`에 넣으세요.
2. GitHub Action 워크플로우를 `workflow_dispatch` 또는 스케줄로 실행하세요.
3. 생성된 CRL은 `your-domain.com/[CRL_NAME].crl`로 게시됩니다.

## 기여
기여를 원하시면 리포지토리를 포크하고 변경을 적용한 뒤 풀 리퀘스트를 보내주세요. 환영합니다!

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.
<details>
  <summary>라이선스 전문</summary>
<pre>
Copyright 2026 concertypin

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
</pre>
</details>
