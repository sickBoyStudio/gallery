# sickBoyStudio / Gallery

팀 이미지를 모아 둔 아카이브입니다.

[Studio](https://github.com/sickBoyStudio) · [Discussions](https://github.com/sickBoyStudio/.github/discussions) · [이미지 등록](https://github.com/sickBoyStudio/gallery/issues/new?template=add-photo.yml)

<!-- GALLERY:START -->
<p align="center"><a href="#group-4">4인 사진 (1)</a> · <a href="#group-6">6인 사진 (1)</a></p>

<a id="group-4"></a>

## 4인 이미지

<p align="center">
<a href="photos/4-devs/2026-10-15-crew.webp"><img src="photos/4-devs/2026-10-15-crew.webp" width="100%" alt="첫 단체 사진"></a><br><sub>첫 단체 사진 · 2026-10-15</sub>
</p>

<a id="group-6"></a>

## 6인 이미지

<p align="center">
<a href="photos/6-devs/2026-10-15-crew.webp"><img src="photos/6-devs/2026-10-15-crew.webp" width="100%" alt="첫 단체 사진"></a><br><sub>첫 단체 사진 · 2026-10-15</sub>
</p>
<!-- GALLERY:END -->

---

## 사진 올리는 법

### Git이 편하면 — PR

1. 인원수에 맞는 폴더에 사진을 넣습니다.
   - 4명: `photos/4-devs/`
   - 6명: `photos/6-devs/`
   - 다른 인원수라면 `photos/<인원수>-devs/` 폴더를 새로 만들면 자동으로 새 섹션이 생깁니다.
2. 파일 이름은 `YYYY-MM-DD-영문-설명.확장자`로 짓습니다. 예: `2026-12-24-christmas-party.webp`
3. 설명을 한글로 달고 싶으면 같은 이름의 `.txt` 파일 첫 줄에 적습니다. 예: `2026-12-24-christmas-party.txt` → `크리스마스 출시 기념`
4. PR을 보내면 파일 형식과 크기를 자동으로 검사하고, merge되면 README가 자동으로 갱신됩니다.

| 규칙 | 내용 |
|---|---|
| 형식 | `.webp` `.jpg` `.png` `.gif` |
| 크기 | 한 장에 5MB 이하 (가능하면 1MB 안팎의 `.webp`) |
| 정렬 | 최신 사진이 위에 크게, 이전 사진은 아래 표로 |

로컬에서 미리 보려면:

```sh
python3 scripts/build_readme.py --check   # 파일 검사
python3 scripts/build_readme.py           # README 갱신
```

### Git이 낯설면 — 이슈

[**이미지 등록** 이슈](https://github.com/sickBoyStudio/gallery/issues/new?template=add-photo.yml)를 열고 사진을 끌어다 놓으세요. 운영진이 폴더에 넣어 드립니다.

## 지켜 주세요

- 사진에 나오는 **모든 사람(또는 그 사람의 아바타)이 공개에 동의**한 사진만 올립니다.
- 다른 사람이 만든 이미지나 캐릭터를 쓴 사진이라면 설명(`.txt`)에 출처를 적어 주세요.
- 이 레포는 **공개**입니다. 얼굴, 학교, 위치처럼 개인정보가 드러나는 사진은 올리지 마세요.
