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

    # 데이터 유효성 확인
    st.write("Order Counts:", order_counts)  # Streamlit에서 데이터가 제대로 있는지 출력 확인

    # 시각화
    plt.figure(figsize=(10, 6))
    
    # 막대그래프 그리기
    if len(order_counts) > 0:  # 값이 있는 경우에만 그래프 그리기
        bars = plt.bar(order_counts.index.astype(str), order_counts.values, color='skyblue')

        # 세로선 제거
        plt.grid(False)
        
        # 각 막대 위에 수치 표시
        for bar in bars:
            yval = bar.get_height()  # 막대의 높이 값(주문 수)
            plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval), ha='center', va='bottom')  # 막대 위에 수치를 표시

        # 가로축 레이블을 동적으로 생성하여 21개로 맞춤 (<1.0, >1.0, >2.0 형태로)
        num_ticks = len(order_counts.index)  # 실제 눈금 수를 기반으로 라벨 생성
        xticks_labels = [f">{i / 10.0:.1f}" if i > 0 else "<1.0" for i in range(num_ticks)]  # 21개 자동 생성

        # 가로축 눈금과 라벨 설정
        plt.xlabel('Order Amount Range')
        plt.ylabel('Order Count')
        plt.title('Order Distribution by Amount')

        # xticks 설정
        plt.xticks(ticks=order_counts.index, labels=xticks_labels, rotation=45)
    else:
        st.write("No data available to display.")  # 데이터가 없을 경우 경고 메시지 출력
    
    # Streamlit에 그래프 표시
    st.pyplot(plt)
else:
    st.write("Upload a CSV file to start the analysis.")
