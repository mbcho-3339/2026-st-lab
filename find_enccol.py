import json
import os
import datetime

# 입력 파일 경로
columns_file = r"e:\workspace_work_202606\tobeencdec\json\신규암호화대상컬럼.json"
targets_file = r"e:\workspace_work_202606\tobeencdec\json\신규암호화대상목록3차TCR.json"

# 출력 파일 경로 (실행일자 붙이기)
today = datetime.datetime.now().strftime("%Y%m%d")
out_file = rf"e:\workspace_work_202606\tobeencdec\find_enccol_tcr_{today}.txt"

def main():
    # 신규암호화대상컬럼.json 읽기
    with open(columns_file, "r", encoding="utf-8") as f:
        columns_data = json.load(f)

    if isinstance(columns_data, list):
        column_names = [col.get("column_name") for col in columns_data if "column_name" in col]
    elif isinstance(columns_data, dict):
        column_names = [columns_data.get("column_name")]
    else:
        column_names = []

    # 신규암호화대상목록3차TCR.json 읽기
    with open(targets_file, "r", encoding="utf-8") as f:
        targets_data = json.load(f)

    if isinstance(targets_data, dict):
        targets_data = [targets_data]

    total_files = 0
    found_files = 0
    not_found_files = 0
    summary_info = []
    found_list = []
    not_found_list = []

    with open(out_file, "w", encoding="utf-8") as out:
        for target in targets_data:
            path = target.get("PATH")
            source_file = target.get("SOURCE_FILE")

            if not path or not source_file:
                continue

            total_files += 1
            file_path = os.path.join(path, source_file)

            out.write(f"PATH: {path}\n")
            out.write(f"SOURCE_FILE: {source_file}\n\n")

            found_columns = set()

            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as sf:
                    for line_num, line in enumerate(sf, start=1):
                        for col in column_names:
                            if col and col.lower() in line.lower():  # 대소문자 무시 검색
                                found_columns.add(col)
                                out.write(f"{source_file} (Line {line_num}): {line.strip()}\n")

            if found_columns:
                found_files += 1
                found_list.append(source_file)
            else:
                not_found_files += 1
                not_found_list.append(source_file)

            summary_info.append(f"{source_file} | {'|'.join(found_columns) if found_columns else 'NO_MATCH'}")

            out.write("\n" + "#" * 100 + "\n\n")

        # 마지막에 요약 정보 출력
        out.write("\n===== SUMMARY =====\n")
        out.write(f"TOTAL SOURCE_FILE: {total_files}\n")
        out.write(f"FOUND FILES: {found_files}\n")
        out.write(f"NOT FOUND FILES: {not_found_files}\n\n")

        out.write("SOURCE_FILE | FOUND_COLUMN_NAME\n")
        out.write("---------------------------------\n")
        for info in summary_info:
            out.write(info + "\n")

        # FOUND FILE LIST 출력
        out.write("\n===== FOUND FILE LIST =====\n")
        for ff in found_list:
            out.write(ff + "\n")

        # NOT FOUND FILE LIST 출력
        out.write("\n===== NOT FOUND FILE LIST =====\n")
        for nf in not_found_list:
            out.write(nf + "\n")

    print(f"완료: {out_file}")

if __name__ == "__main__":
    main()

이 프로그램은 두 개의 JSON 파일을 기반으로 암호화 대상 컬럼(column_name)이 실제 코드 파일(SOURCE_FILE) 안에 존재하는지 자동으로 검사하고, 그 결과를 정리하는 구조입니다. 전체 구성을 단계별로 설명드리면 다음과 같습니다:

📂 입력 파일
신규암호화대상컬럼.json

암호화 대상 컬럼 목록을 담고 있으며, 각 객체에 "column_name" 키가 있습니다.

이 값들이 검색 대상 문자열입니다.

신규암호화대상목록3차TCR.json

검색할 파일들의 메타정보를 담고 있으며, 각 객체에 "PATH"와 "SOURCE_FILE" 키가 있습니다.

"PATH"는 디렉터리 경로, "SOURCE_FILE"은 실제 파일명입니다.

⚙️ 프로그램 처리 흐름
컬럼 목록 읽기

신규암호화대상컬럼.json에서 모든 "column_name" 값을 추출해 리스트로 저장합니다.

검색 대상 파일 목록 읽기

신규암호화대상목록3차TCR.json에서 "PATH"와 "SOURCE_FILE"을 가져와 실제 파일 경로를 구성합니다.

파일별 검색 수행

각 SOURCE_FILE을 열고, 모든 라인을 순회하면서 column_name이 포함되어 있는지 확인합니다.

검색은 대소문자 구분 없이 수행합니다 (col.lower() in line.lower()).

찾은 경우 라인 번호와 함께 원래 라인을 그대로 출력합니다.

파일별 결과 출력

파일별로 맨 위에 PATH와 SOURCE_FILE을 출력합니다.

찾은 라인들은 SOURCE_FILE (Line N): 원래 라인 형식으로 기록합니다.

파일 검색이 끝나면 # 100개를 출력해 구분선을 만듭니다.

📊 요약 정보
검색이 끝난 후 결과 파일(find_enccol_tcr_{today}.txt) 맨 마지막에 요약을 추가합니다:

TOTAL SOURCE_FILE: 전체 파일 수

FOUND FILES: column_name을 찾은 파일 수

NOT FOUND FILES: 못 찾은 파일 수

SOURCE_FILE | FOUND_COLUMN_NAME: 각 파일별로 찾은 컬럼 이름을 |로 구분해 출력 (못 찾은 경우 NO_MATCH)

FOUND FILE LIST: 컬럼을 찾은 파일들의 이름 목록

NOT FOUND FILE LIST: 컬럼을 찾지 못한 파일들의 이름 목록
