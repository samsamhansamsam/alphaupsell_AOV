import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 제목 설정
st.title('Order Amount Distribution')

# 파일 업로더 생성
uploaded_file = st.file_uploader("Upload CSV file", type="csv")

if uploaded_file is not None:
    # 데이터 읽기
    data = pd.read_csv(uploaded_file)

    # '총 주문 금액' 데이터 타입 변환
    data['총 주문 금액'] = pd.to_numeric(data['총 주문 금액'], errors='coerce')

    # 중복 제거: 중복된 '주문번호'가 있을 때 '업셀'을 우선적으로 보존
    data = data.sort_values(by=['일반/업셀 구분'], ascending=True)  # '일반'을 먼저 정렬하여 '업셀'을 남김
    data = data.drop_duplicates(subset=['주문번호'], keep='last')  # '업셀' 우선 보존

    ### 1. 전체 주문 기준 시각화 ###
    st.write("### 전체 주문 기준 객단가 분포")

    # 10,000원 단위로 범주화 (전체 주문 기준)
    data['금액 범주'] = (data['총 주문 금액'] // 10000) * 10000

    # 20만원 이상의 주문들을 200,000원 카테고리에 합치기
    data['금액 범주'] = data['금액 범주'].apply(lambda x: 200000 if x > 200000 else x)

    # 범주별 주문 수 계산 (전체 주문 기준)
    order_counts = data['금액 범주'].value_counts().sort_index()

    # 시각화 (전체 주문 기준)
    plt.figure(figsize=(10, 6))
    bars = plt.bar(order_counts.index, order_counts.values, color='skyblue', width=8000)

    # 각 막대 위에 수치 표시
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval), ha='center', va='bottom')

    # 가로축 라벨 설정
    num_ticks = len(order_counts.index)
    xticks_labels = [f">{i / 10.0:.1f}" if i > 0 else "<1.0" for i in range(num_ticks)]
    plt.xticks(ticks=order_counts.index, labels=xticks_labels, rotation=45)
    plt.xlabel('Order Amount Range')
    plt.ylabel('Order Count')
    plt.title('Order Distribution by Amount (전체 주문 기준)')
    
    # Streamlit에 전체 주문 기준 그래프 표시
    st.pyplot(plt)

    ### 2. 업셀 주문 기준 시각화 ###
    st.write("### 업셀 주문 기준 객단가 분포")

    # 업셀 주문 필터링
    upsell_data = data[data['일반/업셀 구분'] == '업셀']

    # 데이터 검증: 업셀 주문만 필터링된 데이터 출력
    st.write("업셀 주문 데이터 검증:", upsell_data)

    # 10,000원 단위로 범주화 (업셀 주문 기준)
    upsell_data['금액 범주'] = (upsell_data['총 주문 금액'] // 10000) * 10000

    # 20만원 이상의 주문들을 200,000원 카테고리에 합치기
    upsell_data['금액 범주'] = upsell_data['금액 범주'].apply(lambda x: 200000 if x > 200000 else x)

    # 범주별 주문 수 계산 (업셀 주문 기준)
    upsell_order_counts = upsell_data['금액 범주'].value_counts().sort_index()

    # 시각화 (업셀 주문 기준)
    plt.figure(figsize=(10, 6))
    bars = plt.bar(upsell_order_counts.index, upsell_order_counts.values, color='orange', width=8000)

    # 각 막대 위에 수치 표시
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval), ha='center', va='bottom')

    # 가로축 라벨 설정 (업셀 주문 기준)
    num_ticks = len(upsell_order_counts.index)
    xticks_labels = [f">{i / 10.0:.1f}" if i > 0 else "<1.0" for i in range(num_ticks)]
    plt.xticks(ticks=upsell_order_counts.index, labels=xticks_labels, rotation=45)
    plt.xlabel('Order Amount Range')
    plt.ylabel('Order Count')
    plt.title('Order Distribution by Amount (업셀 주문 기준)')

    # Streamlit에 업셀 주문 기준 그래프 표시
    st.pyplot(plt)

else:
    st.write("Upload a CSV file to start the analysis.")
