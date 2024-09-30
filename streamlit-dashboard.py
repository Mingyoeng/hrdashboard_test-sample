import streamlit as st
import pandas as pd
import plotly.express as px

# CSV 파일 로드
@st.cache_data
def load_data():
    data = pd.read_csv('employee_data.csv')
    return data

df = load_data()

# 대시보드 제목
st.title('SK엠앤서비스(주) 직원 대시보드')

# 기본 정보 표시
st.subheader('기본 정보')
st.write(f"총 직원 수: {len(df)}")
st.write(f"부서 수: {df['조직'].nunique()}")

# 성별 분포
st.subheader('성별 분포')
gender_counts = df['성별'].value_counts()
fig_gender = px.pie(values=gender_counts.values, names=gender_counts.index, title='성별 분포')
st.plotly_chart(fig_gender)

# 직군 분포
st.subheader('직군 분포')
job_counts = df['직군'].value_counts()
fig_job = px.bar(x=job_counts.index, y=job_counts.values, title='직군 분포')
st.plotly_chart(fig_job)

# 근무 기간 히스토그램
st.subheader('근무 기간 분포')
df['근무일수'] = pd.to_numeric(df['근무일수(그룹입사일기준)'])
fig_tenure = px.histogram(df, x='근무일수', title='근무일수 분포')
st.plotly_chart(fig_tenure)

# 조직별 직원 수
st.subheader('조직별 직원 수')
org_counts = df['조직'].value_counts()
fig_org = px.bar(x=org_counts.index, y=org_counts.values, title='조직별 직원 수')
st.plotly_chart(fig_org)

# 채용 구분별 직원 수
st.subheader('채용 구분별 직원 수')
hire_counts = df['채용구분'].value_counts()
fig_hire = px.pie(values=hire_counts.values, names=hire_counts.index, title='채용 구분별 직원 수')
st.plotly_chart(fig_hire)

# 직원 목록 (필터링 가능)
st.subheader('직원 목록')
selected_columns = ['사번', '성명', '조직', '직군', '직책', '호칭', '성별', '입사일']
st.dataframe(df[selected_columns])
