import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 제목 설정
st.title('주문 금액별 주문 수 분석')

# 파일 업로더 생성
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type="csv")

if uploaded_file is not None:
    # 데이터 읽기
    data = pd.read_csv(uploaded_file)

    # '총 주문 금액' 데이터 타입 변환
    data['총 주문 금액'] = pd.to_numeric(data['총 주문 금액'], errors='coerce')

    # 10,000원 단위로 범주화
    data['금액 범주'] = (data['총 주문 금액'] // 10000) * 10000
    order_counts = data['금액 범주'].value_counts().sort_index()

    # 범위 제한 (0 ~ 200,000원)
    order_counts = order_counts[order_counts.index <= 200000]

    # 시각화
    plt.figure(figsize=(10, 6))
    plt.bar(order_counts.index.astype(str), order_counts.values, color='skyblue')
    plt.xlabel('price range (won)')
    plt.ylabel('order count')
    plt.title('금액대별 객단가 분포')
    plt.xticks(rotation=45)
    plt.grid(True)
    
    # Streamlit에 그래프 표시
    st.pyplot(plt)
else:
    st.write("CSV 파일을 업로드하여 분석을 시작하세요.")
