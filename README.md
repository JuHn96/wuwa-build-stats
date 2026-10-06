# Wuwa Build Stats

명조 캐릭터 빌드 데이터를 수집하고 통계화하여 제공하는 개인 포트폴리오 프로젝트입니다.

## 학습 기록
상세한 학습 내용과 진행 과정은 Notion에서 확인할 수 있습니다.  
[Notion](https://acute-throne-23e.notion.site/3ea8cae706e680a995bfef442c48aac1)

# 커밋 메세지 관련

feat: 기능 추가
fix: 버그 수정
docs: 문서 수정
chore: 설정/환경 작업
refactor: 구조 개선
test: 테스트 추가/수정

## Tech Stack

### Backend
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL

### Web
- Next.js
- TypeScript
- Tailwind CSS

### Android
- Kotlin
- Jetpack Compose

### Infrastructure
- Docker
- Docker Compose
- GitHub Actions

## Deployment

초기에는 무료 배포 환경을 사용하고,
이후 AWS로 마이그레이션하는 것을 목표로 합니다.

## Status

Development environment setup in progress.

## Master Data 검증

로컬 Master Data와 이미지 파일의 정합성을 검사하기 위한 스크립트입니다.

### 대상

- `data/game-data/characters.json`
- `data/game-data/weapons.json`
- `data/game-data/echoes.json`
- `data/img/characters/`
- `data/img/weapons/`
- `data/img/echoes/`

실제 Master JSON과 이미지 파일은 Git에 포함하지 않습니다.

### 실행

프로젝트 루트에서 실행합니다.

```bash
python3 scripts/validate_master_data.py
