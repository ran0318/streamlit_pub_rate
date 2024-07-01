import streamlit as st 
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt


import nltk
nltk.download('stopwords')


st.title("금리 관련 기사 검색 결과")

st.write('사이드바를 이용하여 기사를 검색해보세요!')

# 사이드바 
with st.sidebar :
   
  sdt = st.date_input("시작일자를 선택하세요", pd.to_datetime("2024-03-01"))
  edt = st.date_input("종료일자를 선택하세요", pd.to_datetime("2024-05-31"))
  upndown = st.text_input("up, down 중 하나를 입력하세요", "up or down")

# 데이터 불러오기
news = pd.read_csv("streamlit_news_final.csv", parse_dates=['date'],encoding='utf-8')
df = pd.DataFrame(news)

# 시작일자와 종료일자를 datetime 형식으로 변환
sdt = pd.Timestamp(sdt)
edt = pd.Timestamp(edt)


# 날짜 필터링
filtered_df = df[(df['date'] >= sdt) & (df['date'] <= edt)]
filtered_df['date'] = filtered_df['date'].dt.strftime("%Y-%m-%d")  
# 날짜를 문자열로 변환하여 필터링된 데이터프레임 출력
# 'date' 열을 문자열로 변환하여 'YYYY-MM-DD' 형식으로 표시


# 'updown' 컬럼에서 'up' 또는 'down' 값인 행 필터링
if upndown == 'up':
    filtered_df = filtered_df[filtered_df['up-down'] == 'up']
else:
    filtered_df = filtered_df[filtered_df['up-down'] == 'down']

# 필터링된 데이터프레임의 갯수 출력
st.write(f"검색된 기사 수: {filtered_df.shape[0]} 개")

st.write('검색된 기사의 본문으로 워드 클라우드를 만들었습니다.')

# 워드클라우드 생성
if filtered_df.shape[0] > 0:
    # 기사 본문을 모두 합치기
    text = ' '.join(filtered_df['text'].tolist())
    #폰트
    plt.rcParams['font.family'] = 'Gulim'
    
    # 워드클라우드 생성 및 표시
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot()

else:
    st.write("검색된 기사가 없습니다.")



# 필터링된 데이터 출력
st.dataframe(filtered_df)


# 다운로드 버튼 연결
st.download_button(
    label='CSV로 다운로드',
    data=df.to_csv(), 
    file_name='newslist.csv', 
    mime='text/csv'
)

