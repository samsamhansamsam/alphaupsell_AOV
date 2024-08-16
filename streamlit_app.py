import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import platform

# 나눔고딕 폰트 설정
if platform.system() == 'Windows':
    plt.rc('font', family='NanumGothic')  # Windows용
elif platform.system() == 'Darwin':  # MacOS의 경우
    plt.rc('font', family='AppleGothic')  # 또는 'NanumGothic' 수동 설치 가능
else:  # Linux (Ubuntu)
    plt.rc('font', family='NanumGothic')

# 마이너스 기호가 깨지지 않게 설정
plt.rcParams['axes.unicode_minus'] = False

# 제목 설정
st.title('주문 금액별 주문 수 분석')

# 파일 업로더 생성
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type="csv")

if uploaded_file is not None:
    # 데이터 읽기
    data = pd.read_csv(uploaded_file)

    # '주문번호' 열을 기준으로 중복 제거
    data = data.drop_duplicates(subset=['주문번호'])

    # '총 주문 금액' 데이터 타입 변환
    data['총 주문 금액'] = pd.to_numeric(data['총 주문 금액'], errors='coerce')

    # 10,000원 단위로 범주화
    data['금액 범주'] = (data['총 주문 금액'] // 10000) * 10000

    # 20만원 이상의 주문들을 200,000원 카테고리에 합치기
    data['금액 범주'] = data['금액 범주'].apply(lambda x: 200000 if x > 200000 else x)
    
    # 범주별 주문 수 계산
    order_counts = data['금액 범주'].value_counts().sort_index()

    # 시각화
    plt.figure(figsize=(10, 6))
    bars = plt.bar(order_counts.index.astype(str), order_counts.values, color='skyblue')
    
    # 세로선 제거
    plt.grid(False)
    
    # 각 막대 위에 수치 표시
    for bar in bars:
        yval = bar.get_height()  # 막대의 높이 값(주문 수)
        plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval), ha='center', va='bottom')  # 막대 위에 수치를 표시
    
    plt.xlabel('금액 범주 (원)')
    plt.ylabel('주문 수')
    plt.title('0 ~ 200,000원 단위별 주문 수')
    plt.xticks(rotation=45)
    
    # Streamlit에 그래프 표시
    st.pyplot(plt)
else:
    st.write("CSV 파일을 업로드하여 분석을 시작하세요.")
