import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("📘 충남대 시간표 추천 앱")

uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.sidebar.header("🛠️ 조건 설정")
    major = st.sidebar.selectbox("전공 선택", df["운영학과"].unique())
    preferred_days_off = st.sidebar.multiselect("공강 원하는 요일", ["월", "화", "수", "목", "금"])
    preferred_mode = st.sidebar.radio("수업 형태", ["전체", "대면강의", "화상강의"])
    grading_type = st.sidebar.radio("평가 방식", ["전체", "상대평가", "절대평가"])

    # 필터링
    filtered = df[df["운영학과"] == major]
    if preferred_mode != "전체":
        filtered = filtered[filtered["수업형태"] == preferred_mode]
    if grading_type != "전체":
        filtered = filtered[filtered["성적평가방식"] == grading_type]
    if preferred_days_off:
        pattern = "|".join(preferred_days_off)
        filtered = filtered[~filtered["강의시간"].str.contains(pattern)]

    st.success(f"🔍 총 {len(filtered)}개의 강의가 조건에 맞습니다.")
    st.dataframe(filtered)

    # 시간표 이미지로 출력 (간단 버전)
    st.subheader("📅 시간표 미리보기")

    time_slots = ["9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"]
    days = ["월", "화", "수", "목", "금"]
    timetable = pd.DataFrame("", index=time_slots, columns=days)

    for _, row in filtered.iterrows():
        name, times = row["과목명"], row["강의시간"].split(",")
        for t in times:
            day = t[0]
            if day in timetable.columns:
                time = t[1:]
                timetable.loc[time, day] = name

    st.dataframe(timetable.fillna(""))
else:
    st.info("왼쪽에서 CSV 파일을 업로드해주세요.")
