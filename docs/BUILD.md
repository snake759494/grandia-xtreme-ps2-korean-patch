# 재빌드

## 준비
- Python 3, `pip install numpy numba Pillow`
- 저장소 최상위에 원본 `Grandia Xtreme (Japan, Asia).iso`(MD5 `8f41f39e270d2a2b7b148e680b39c086`)와 글꼴(`docs/FONT_CREDITS.md`)
- xdelta3 (`xdelta.exe`)

## 빌드
```powershell
python tools/prepare.py     # 원본 ISO에서 extract/·dec/ 추출, 글꼴·텍스처 목록, 원문 목록 생성, 번역 복원(translation/src, translation/ko)
python tools/build.py       # → "Grandia Xtreme (Japan, Asia) (Korean).iso"
```
`prepare.py`는 마지막에 `missing = 0`을 출력해야 합니다. 이 순서로 만든 ISO는 릴리즈 xdelta를 적용한 결과와 바이트 단위로 같습니다.

번역을 고칠 때는 `translation/ko/*.tsv`를 고치고 `python tools/check_tr.py translation/src/mdt_00.tsv translation/ko/mdt_00.tsv`로 줄 길이·제어 토큰을 검사한 뒤 다시 빌드합니다. 공개용 `translation/pub`과 `tools`는 `python tools/export_public.py <폴더>`로 만듭니다.

## 차분 파일
```powershell
.\xdelta.exe -e -0 -S none -A -s "Grandia Xtreme (Japan, Asia).iso" "Grandia Xtreme (Japan, Asia) (Korean).iso" Grandia_Xtreme_PS2_KO_v1.0.xdelta
```

## 파일
- `translation/pub/mdt_00~25.tsv`: 대사, `sys_00~03.tsv`: 아이템·마법·스킬·메뉴 등 시스템 문자열, `desc_groups.tsv`: 4줄 설명 묶음, `enemy.tsv`: 적 이름·적 기술 이름 (모두 `ID	원문 SHA-1 앞 16자리	번역`)
- `translation/charmap_jp.txt`: 원본 글꼴의 글리프 순서
- `tools/build.py`: 전체 빌드. `mdtbuild.py`·`msg.py`·`vm.py` 대사 스크립트, `sysbuild.py`·`sysgroups.py`·`menu_ko.py` GRXSYS, `bintext.py` 전투, `enemy.py` 적 이름, `code16.py` 미니게임, `ko.py`·`mkfont.py` 글꼴, `tex*.py` 그림 글자, `lz.py`·`lzfast.py` 압축, `isofs.py`·`ext.py` 디스크
- `tools/prepare.py`·`jppool.py`·`export_public.py`: 원문 없이 재빌드하기 위한 스크립트
