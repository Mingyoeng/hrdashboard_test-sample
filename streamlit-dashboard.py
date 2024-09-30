import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# CSV 파일 로드
@st.cache_data
def load_data():
    data = pd.read_csv('employee_data.csv')
    return data

# 데이터 로드
df = load_data()

# 페이지 설정
st.set_page_config(page_title="SK엠앤서비스(주) 직원 대시보드", layout="wide")

# 대시보드 제목
st.title('SK엠앤서비스(주) 직원 대시보드')

# 기본 정보 표시
st.header('기본 정보')
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("총 직원 수", len(df))
with col2:
    st.metric("부서 수", df['조직'].nunique())
with col3:
    st.metric("평균 근속 연수", f"{df['근무일수(그룹입사일기준)'].astype(int).mean() / 365:.1f}년")

# 성별 분포
st.header('성별 분포')
gender_counts = df['성별'].value_counts()
st.bar_chart(gender_counts)

# 직군 분포
st.header('직군 분포')
job_counts = df['직군'].value_counts()
st.bar_chart(job_counts)

# 근무 기간 히스토그램
st.header('근무 기간 분포')
df['근무년수'] = df['근무일수(그룹입사일기준)'].astype(int) / 365
fig, ax = plt.subplots()
ax.hist(df['근무년수'], bins=20, edgecolor='black')
ax.set_xlabel('근무 년수')
ax.set_ylabel('직원 수')
st.pyplot(fig)

# 조직별 직원 수
st.header('조직별 직원 수')
org_counts = df['조직'].value_counts()
st.bar_chart(org_counts)

# 채용 구분별 직원 수
st.header('채용 구분별 직원 수')
hire_counts = df['채용구분'].value_counts()
st.bar_chart(hire_counts)

# 직원 목록 (필터링 가능)
st.header('직원 목록')
selected_columns = ['사번', '성명', '조직', '직군', '직책', '호칭', '성별', '입사일']
st.dataframe(df[selected_columns])

# 필터링 옵션
st.sidebar.header('필터링 옵션')
selected_org = st.sidebar.multiselect('조직 선택', options=df['조직'].unique())
selected_job = st.sidebar.multiselect('직군 선택', options=df['직군'].unique())

# 필터링 적용
if selected_org or selected_job:
    filtered_df = df[
        (df['조직'].isin(selected_org) if selected_org else True) &
        (df['직군'].isin(selected_job) if selected_job else True)
    ]
    st.subheader('필터링된 직원 목록')
    st.dataframe(filtered_df[selected_columns])

# 추가 통계
st.header('추가 통계')
col1, col2 = st.columns(2)
with col1:
    st.subheader('직책별 평균 근속 연수')
    avg_tenure_by_position = df.groupby('직책')['근무일수(그룹입사일기준)'].mean() / 365
    st.bar_chart(avg_tenure_by_position)

with col2:
    st.subheader('성별 직군 분포')
    gender_job_dist = df.groupby(['성별', '직군']).size().unstack()
    st.bar_chart(gender_job_dist)
